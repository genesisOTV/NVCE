import json
import collections
import thesaurus as th


#Main regex engine: Standardizes synonyms and semantically parses headlines
class PoserArrays(object):
    
    PCatalogue = [
        ["Filler"],
        ["a"],
        ["of", "to", "on", "in", "is", "at", "by", "as", "an"],
        ["for", "are", "all", "and", "the", "did", "was"],
        ["from", "goes", "with", "will", "over", "into", "been", "when", "then", "than", "were", "that", "near", "what"],
        ["under", "would", "those", "could", "after", "there", "about", "which"],
        ["should", "during", "unless", "inside"],
        ["through", "outside"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"],
        ["Filler"]
        ]
    
    
    
    #Parses new headlines; assembles FHl
    def build_FHl(self, Hl):
        FHl = [[], [], []]

        #Splits headline into proper nouns, verbs, misc.
        for i, word in enumerate(Hl):
            baseVerb = PoserArrays.search_PVC(self, word)

            if baseVerb:
                FHl[1].append(baseVerb)
            else:
                if not PoserArrays.search_PC(self, word):
                    FHl[2].append(word)
            
        if not FHl[1]:
            #Runs thesaurus check if no verbs are detected
            PoserArrays.searchThesaurus(self, FHl[2])

        return FHl
        
    
    
    """Search methods:"""
    #PVC Search
    def search_PVC(self, working_word):
        PVCD = json.load(open("PVCDictionary.json"))
        PVCatalogue = PVCD["PVC"]
        index = len(working_word)
        baseWord = None
        if(index <= 12):
            wl_dict = PVCatalogue[str(index)]
            if working_word in wl_dict:
                baseWord = wl_dict[working_word]
                if(baseWord):
                    print("Poser Verb found in catalogue: " + working_word + ", " + baseWord)
        else:
            wl_dict = None
        
        return baseWord
    
    #PC Search
    def search_PC(self, working_word):
        index = len(working_word)
        wl_array = self.PCatalogue[index]

        found = False
        for a in wl_array:
            raw_word = a
            if raw_word == working_word:
                print("Preposition found in catalogue: " + working_word)
                found = True
                
                break
        
        return found
    
    
    
    #Finds potential verbs within given text excerpt;
    #Automatically serializes new verbs to PVC
    def searchThesaurus(self, Excerpt):
        print("THESAURUS CHECK")
        verbCandidates = {}
        #Iterates for word in headline
        for word in Excerpt:
            thWord = th.Word(word)
            #Finds verb synonyms
            vSynonyms = thWord.synonyms('all', partOfSpeech=th.POS_VERB, allowEmpty=False)
            if vSynonyms:
                print("Candidate found")
                #Finds noun synonyms
                nSynonyms = thWord.synonyms('all', partOfSpeech=th.POS_NOUN, allowEmpty=False)
                if not nSynonyms:
                    print("Nonambiguous verb found")
                    verbCandidates = {word: vSynonyms}
                    break
                else:
                    verbCandidates[word] = vSynonyms
        
        for verb in verbCandidates.keys():
            baseForm = ""
            isPVerb = False
            synonyms_raw = verbCandidates[verb]
            Synonyms = self.deArray(synonyms_raw)
            
            #Adds word and recognized synonym version to PVC
            for synonym in Synonyms:
                serializedForm = self.search_PVC(synonym)
                if serializedForm:
                    isPVerb = True
                    baseWord = serializedForm
                    break
            if isPVerb:
                self.addWord([verb, baseWord])
                print(verb + ", " + baseWord)
                break
            else:
                print("Base form not found of: " + verb)
        
        print("CHECK COMPLETED")
    
    #Recursive method to extract strings from jagged arrays
    def deArray(self, jArray):
        rtrnArray = []
        for subItem in jArray:
            if type(subItem) is list:
                words = []
                words = self.deArray(subItem)
                rtrnArray.extend(words)
            elif isinstance(subItem, str):
                rtrnArray = jArray
                break
    
        return rtrnArray
    
    
    
    #Adds verb pair (verb, base verb) to PVC
    def addWord(self, wordPair):
        PVCDinst = json.load(open("PVCDictionary.json"))
        PVC = PVCDinst["PVC"]
        ind = len(wordPair[0])
        PVC[str(ind)][wordPair[0]] = wordPair[1]
        PVCDinst["PVC"] = PVC
        with open("PVCDictionary.json", "w") as jsonFile:
            json.dump(PVCDinst, jsonFile)
        print("PVCDictionary updated")
        




#LEGACY METHOD
"""
def tempPVCDCompiler(self):
    jsonPVCD = json.load(open("PVCDictionary.json"))
    PVCDictionary = jsonPVCD["PVC"]

    for n, lenCategory in enumerate(self.PVCatalogue):
        i = str(n)
        print(i)
        lenPVCD = PVCDictionary[i]
        for wordPair in lenCategory:
            lenPVCD[wordPair[0]] = wordPair[1]
        PVCDictionary[i] = lenPVCD
    jsonPVCD["PVC"] = PVCDictionary
        
    with open("PVCDictionary.json", "w") as rtrnFile:
        json.dump(jsonPVCD, rtrnFile)

    print("Transfer complete")
"""

