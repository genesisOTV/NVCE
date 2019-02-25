import json as jsonPlug

import poserArrays_Limbo

#headline_file = open("headline.txt", "r")
#HL = headline_file.read()

#Splits provided headline and standardizes language
def semParseHl(Hl):
    rawSplit_Hl = Hl.split()
    split_Hl = punctParse(rawSplit_Hl)
    properNouns = findPNouns_Primary(split_Hl)
    #print(properNouns)
    
    filteredSHl = []
    if(properNouns):
        filteredSHl = removePNouns(split_Hl, properNouns)
    
    #print("Reached")
    filteredSHl = [x.lower() for x in filteredSHl]
    #print(split_Hl)

    #Performs synonym standardization (See poserArrays_Limbo.py)
    instance = poserArrays_Limbo.PoserArrays()

    finalParse = instance.build_FHl(filteredSHl)
    Verbs = finalParse[1]
    nonVerbs = finalParse[2]
    #print(parsedHl)

    #HlRemainder = []
    #if properNouns:
    #   HlRemainder = removePNouns(nonVerbs, properNouns)
    #print("NOUNS: ")
    #print(HlNouns)
    
    finalParse[0] = properNouns
    #filteredHl[2] = HlRemainder
    
    #rtrn = [parsedHl, properNouns]

    return finalParse


def findPNouns_Primary(splitHl):
    pNouns = []
    #recheckNeeded = [splitHl[0]]
    recheckNeeded = []
    #print(splitHl)
    for i, word in enumerate(splitHl):
        wordArray = list(word)
        
        if(wordArray[0] == wordArray[0].upper()):
            #print("Potential proper noun found: " + word)
            if not word in pNouns:
                #if(word != recheckNeeded[0]):
                pNouns.append(word)
        

    if(len(pNouns) == len(splitHl)):
        print("Every word in headline capitalized, resorting to secondary pNoun detection")
        pNouns = []
        recheckNeeded.extend(splitHl)
    else:
        PNDictJson = jsonPlug.load(open("properNouns.json"))
        registeredPNs = PNDictJson["VerifiedPNouns"]
        for pNoun in pNouns:
            if not pNoun in registeredPNs:
                registeredPNs.append(pNoun)

        PNDictJson["VerifiedPNouns"] = registeredPNs
        with open("properNouns.json", "w") as pnFile:
            jsonPlug.dump(PNDictJson, pnFile)
    
    recheckedPNs = findPNouns_Secondary(recheckNeeded)
    if recheckedPNs:
        for PN in recheckedPNs:
            pNouns.insert(0, PN)
    
    return pNouns

def punctParse(splitHl):
    parsedSplit = []
    for i, word in enumerate(splitHl):
        wordArray = list(word)
        firComp = ""
        secComp = ""
        if("-" in wordArray):
            i = wordArray.index("-")
            firComp = "".join(wordArray[:i])
            secComp = "".join(wordArray[(i+1):])
            print(firComp)
            print(secComp)
            print("flag")
            
            #splitHl[i] = firComp
            #splitHl.insert(i, secComp)
            
            word = firComp
            wordArray = list(word)
        
        if("." in wordArray):
            word = removePeriods(wordArray)
            wordArray = list(word)
            #splitHl[i] = word
            #print(word)
        if("." in list(secComp)):
            secArray = list(secComp)
            secComp = removePeriods(secArray)
        parsedSplit.append(word)
        if secComp:
            parsedSplit.append(secComp)
    return parsedSplit

def removePeriods(chars):
    parsedWord = ""
    i = chars.index(".")
    iteratedComp = "".join(chars[:i])
    
    remainder = chars[(i+1):]
    parsedRemainder = ""
    if(i < (len(chars) - 1)):
        if("." in remainder):
            parsedRemainder = removePeriods(remainder)
        else:
            parsedRemainder = "".join(remainder)
    
    parsedWord = iteratedComp + parsedRemainder
    return parsedWord


def findPNouns_Secondary(splitHl):
    pNouns = []
    PNDictJson = jsonPlug.load(open("properNouns.json"))
    registeredPNs = PNDictJson["VerifiedPNouns"]

    for word in splitHl:
        if word in registeredPNs:
            pNouns.append(word)
    
    return pNouns

def removePNouns(wordList, pNs):
    for pNoun in pNs:
        try:
            wordList.remove(pNoun)
        except ValueError:
            print("Proper noun discrepancy")
            pass

    return wordList

"""
def removePNouns(wordList, pNs):
    revisedNouns = []
    del pNs[0]
    for subArray in wordList:
        for pNoun in pNs:
            pNoun = pNoun.lower()
            try:
                subArray.remove(pNoun)
            except ValueError:
                pass
        revisedNouns.append(subArray)

    return revisedNouns
"""           

def punctParse_Limbo(splitHl):
    openQuote = False
    resolvedHl = []
    for word in splitHl:
        if(word.isalpha()):
            wordArray = list(word)
            wordHldr = word
            if not openQuote:
                if(wordArray[0] == "'"):
                    wordHldr = word.replace("'", "")
                    openQuote = True
                else:
                    wordHldr = word
            else:
                if(wordArray[-1] == "'"):
                    wordHldr = word.replace("'", "")
                    openQuote = False

            if not wordArray[-1].isalpha():
                wordHldr = word.replace(wordArray[-1], "")
            if(len(wordArray) >= 3):
                if(wordArray[-2] == "'"):
                    wordHldr = word.replace("'s", "")
        
            resolvedHl.append(wordHldr)

    #print(resolvedHl)
    return resolvedHl
            
            
            


#semParseHl("Video appears to show police standoff with suspect")

#"""for word in split_HL:
    #instance = poserArrays1.PoserArrays()
    #instance.search_catalogue(word, False)
    #print("")"""
