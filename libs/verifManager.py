#Local Imports
import testRSSParser
import regex
import thesaurus as th
import poserArrays_Limbo as pvDict
import verifFunctions as verifier

#System Imports
import json
import collections

#Frontend and Backend integration
from django.conf import settings
import sys
sys.path.append(r'D:/Documents/Python/NVCE/NVCEWeb')
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'NVCEWeb.settings'
django.setup()
from feed.models import Source

def accessDB():
    db = Source.objects.all()
    data = {}

    for outlet in db:
        name = outlet.name
        url = outlet.url
        data[name] = url
        
    with open('libs/rssFeeds.json', 'w') as outfile:
        json.dump(data, outfile)

def getRSSFeeds():
    accessDB()
    RSSDict = json.load(open("libs/rssFeeds.json"))
    return RSSDict

#Oversees verification for any updated RSS feeds
def displayAll():
    newHlPack = {}

    updatedFeed = False

    #Retrieves latest instance of trending headlines list
    Hls_Instance = json.load(open("libs/HlInfo.json"))
    LimboPHlDump = Hls_Instance["ParsedHls_Limbo"]
    rssFeeds = getRSSFeeds()
    
    #Iterates for RSS feed (To be changed)
    for i, outlet in enumerate(rssFeeds.keys()):
        print(outlet)
        #Parses new headlines in feed
        Hls, pHls = parseFeed(outlet, rssFeeds)

        if Hls:
            if not updatedFeed:
                updatedFeed = True
            #Stores new headlines (parsed) for short term external access
            LimboPHlDump[outlet]["PHls"] = pHls
            LimboPHlDump[outlet]["Hls"] = Hls
            indFiller = len(pHls) * [-1]
            LimboPHlDump[outlet]["HlsSpecInds"] = indFiller
            
            #Publishes new headlines to proper noun table of contents for verif references
            publishToPNTOC(pHls, outlet)
        
    if updatedFeed:
        saveInst = json.load(open("libs/HlInfo.json"))
        #Submits changes to trendingHls json file
        saveInst["ParsedHls_Limbo"] = LimboPHlDump
        with open("HlInfo.json", "w") as Hls_json:
            json.dump(saveInst, Hls_json)
        
        #Submits new headlines for verification
        sortedCoeffs = verifier.verifyQueuedHls()

        #Moves short term headlines to permanent storage
        moveToTHls(sortedCoeffs)
    


#Displays (10) most recent headlines from provided outlet RSS feed
def parseFeed(outlet, rssFeeds):
    #Parses provided feed
    rssFeed = rssFeeds[outlet]
    newHls = testRSSParser.checkFeed(rssFeed)

    #Splits new headlines into regex format (See regex.py)
    newPHls = []
    newPNs = []
    tempCoeffs_rtrn = []
    if newHls:
        for hl in newHls:
            print(hl)
            
            parsedHl = regex.semParseHl(hl)

            newPHls.append(parsedHl)
        
    
    
    return(newHls, newPHls)



#Adds new (parsed) headlines to proper noun table of contents (pNToC) for verification
def publishToPNTOC(newPHls, source):
    for packet in newPHls:
        pNouns = packet[0]
        HlElems = [source, packet[1], packet[2]]
        Hls_Instance = json.load(open("libs/HlInfo.json"))
        pNounInfo = Hls_Instance["Hls_General_pNouns"]

        pNounInfo["hlArchive"].append(HlElems)
        hlIndex = len(pNounInfo["hlArchive"]) - 1
        #Sets references in PNToC from hlArchive to ToC accordingly
        for pNoun in pNouns:
            References = []
            #Stores
            if pNoun in pNounInfo["pNToC"]:
                References = pNounInfo["pNToC"][pNoun]
                try:
                    References.append(hlIndex)
                except:
                    print(pNoun)
                    #print(pNounInfo["pNToC"])
            else:
                References = [hlIndex]
            pNounInfo["pNToC"][pNoun] = References

        Hls_Instance["Hls_General_pNouns"] = pNounInfo
        #print(Hls_Instance["Hls_General_pNouns"])
        
        with open("libs/HlInfo.json", "w") as Hls_json:
            json.dump(Hls_Instance, Hls_json)
            #print("\n***DUMPED***\n")

#Transfers limbo headlines to trending after verification
def moveToTHls(Coeffs):

    THls_inst = json.load(open("libs/trendingHls.json"))
    Hls_inst = json.load(open("libs/HlInfo.json"))
    pHl_Limbo = Hls_inst["ParsedHls_Limbo"]
    Hls_dict = Hls_inst["Hls_Spec"]
    tHls_dict = THls_inst["TrendingHls_Spec"]
    for source in Coeffs.keys():
        siteCoeffs = Coeffs[source]
        Hls_spec = Hls_dict[source]
        tHls_spec = tHls_dict[source]
        siteLimbo = pHl_Limbo[source]
        Hls = siteLimbo["Hls"]
        PHls = siteLimbo["PHls"]

        savedHls = []
        savedPHls = []
        RefInds = []
        for i, Hl in enumerate(Hls):
            coeff = siteCoeffs[i]
            HlPacket = [Hl, coeff]
            
            tHls_spec.append(HlPacket)
            
            refInd = siteLimbo["HlsSpecInds"][i]
            if(coeff != 0):
                if(refInd == -1):
                    Hls_spec.append(HlPacket)
                else:
                    #refInd = siteLimbo["HlsSpecInds"][i]
                    Hls_spec[refInd] = HlPacket
            else:
                savedPHls.append(PHls[i])
                savedHls.append(Hl)
                if(refInd == -1):
                    RefInds.append(len(Hls_spec))
                    Hls_spec.append(HlPacket)
                else:
                    RefInds.append(refInd)
        
        pHl_Limbo[source] = {"PHls": savedPHls, "Hls": savedHls, "HlsSpecInds": RefInds, "tHlsSpecInds": []}
        Hls_dict[source] = Hls_spec
        tHls_dict[source] = tHls_spec
        
    Hls_inst["ParsedHls_Limbo"] = pHl_Limbo
    Hls_inst["Hls_Spec"] = Hls_dict
    THls_inst["TrendingHls_Spec"] = tHls_dict
    
    with open("libs/HlInfo.json", "w") as Hls_json:
        json.dump(Hls_inst, Hls_json)
    with open("libs/TrendingHls.json", "w") as tHls_json:
        json.dump(THls_inst, tHls_json)

#accessDB()
displayAll()











    
