import json
import collections

import thesaurus as th
import poserArrays_Limbo as pvDict

#"""TRANSFER TO SEPARATE FILE"""
def verifyQueuedHls():
    Hl_file = json.load(open("HlInfo.json"))
    #!MOVE TO FOR LOOP FOR VERIF FACTOR AUTHENTICATION!
    PNReferences = Hl_file["Hls_General_pNouns"]
    PNToC = PNReferences["pNToC"]
    hlArchive = PNReferences["hlArchive"]
    
    QueuedHls = Hl_file["ParsedHls_Limbo"]
    verifCoeffs = {}
    for outlet in QueuedHls.keys():
        hlPacket = QueuedHls[outlet]
        qPHls = hlPacket["PHls"]
        qHls = hlPacket["Hls"]
        
        for i, qPHl in enumerate(qPHls):
            Validated = False
            verifCoeff = 0
            pNouns = qPHl[0]
            hlElems = [qPHl[1], qPHl[2]]

            if not hlElems[1]:
                verifCoeff = -1

            matchedPNInds = []
            for pNoun in pNouns:
                if pNoun in PNToC:
                    pNInds = PNToC[pNoun]
                    matchedPNInds.extend(pNInds)

            if matchedPNInds:
                """
                orderedMNPInds = {}
                totalTally = 0
                for ind in matchedPNInds:
                    if(totalTally < len(matchedPNInds)):
                        occurances = matchedPNInds.count(ind)
                        if orderedMNPInds[occurances]:
                            orderedMNPInds[occurances].extend(ind)
                        else:
                            orderedMNPInds[occurances] = [ind]
                    else:
                        break
                """
                #directory = []
                indDict = {}
                tally = 0
                for ind in matchedPNInds:
                    if(tally < len(matchedPNInds)):
                        if not ind in list(indDict.values()):
                            count = matchedPNInds.count(ind)
                            try:
                                indDict[count].append(ind)
                            except:
                                indDict[count] = [ind]
                    else:
                       break
                
                
                order = list(indDict.keys())
                order.sort()
                for Count in order:
                    sortedInds = indDict[Count]
                    for ref in sortedInds:
                        compareHl = hlArchive[ref]
                        if not (compareHl[0] == outlet):
                            compareVerbs = compareHl[0]
                            Verbs = qPHl[1]
                            verbMatch = 0
                            for verb in Verbs:
                                if verb in compareVerbs:
                                    verbMatch += 1

                            #!REMOVE BREAK FOR INCREASED ACCURACY!
                            """FLAGGED FOR REFORM"""
                            if(verbMatch > 0):
                                coeff_a = verbMatch/compareVerbs
                                coeff_b = verbMatch/Verbs
                                coeff = max(coeff_a, coeff_b)
                                if(coeff >= 2/5):
                                    Validated = True
                                    verifCoeff = 1
                                    break
                                
                    if Validated:
                        break
                
            if(i == 0):
                verifCoeffs[outlet] = [verifCoeff]
            else:
                verifCoeffs[outlet].append(verifCoeff)
        
    #!UPDATE PNTOC REFERENCES WITH COEFFS!
    """FLAGGED FOR REFORM"""
    return verifCoeffs

