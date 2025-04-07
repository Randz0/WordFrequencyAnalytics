editedOutPunctuation = {"." : " ", "," : " ", "!" : " ", ":" : " ", ";" : " ", "?" : " ", "\n" : " "}

class CachedFile:
    def __init__(self, fileName):
        self.fileName = fileName
        self.currentTokenizedWords = []

        self.isCaseSensitive = True

        self.wordsToFrequency = {}
        self.allLowerWordsToFrequency = {}

        self.byFreqWordsToFrequency = [] # Both of these data structures are list of tuples (word --> ocurrences)
        self.allLowerByFreqWordsToFreq = []

        self.byFreqWordsToFreqInUse = []

        self.plotBounds = (0, 0)

        self.blacklist = []
        self.allLowerBlacklist = []

        self.blacklistInUse = []

    def GetAppearencesOfWord(self, wordLookingFor: str):
        listSearchingFrom = self.wordsToFrequency if self.isCaseSensitive else self.allLowerWordsToFrequency
        wordLookingFor = wordLookingFor if self.isCaseSensitive else wordLookingFor.lower()

        if not wordLookingFor in listSearchingFrom:
            return 0

        return listSearchingFrom[wordLookingFor]

    def WordIsInOutputData(self, word):
        return not word in self.blacklistInUse

    def FetchWordsToFrequencies(self):
            self.byFreqWordsToFreqInUse = self.byFreqWordsToFrequency if self.isCaseSensitive else self.allLowerByFreqWordsToFreq
            self.blacklistInUse = self.blacklist if self.isCaseSensitive else self.allLowerBlacklist

            wordsWithinBounds = []
            frequenciesWithinBounds = []

            numberOfWordsToFetch = self.plotBounds[1] - self.plotBounds[0]

            index = self.plotBounds[0] - 1
            stopIndex = self.plotBounds[0] + numberOfWordsToFetch

            currentWordFreqPair = ("", 0)

            while index < stopIndex:
                index += 1

                if index >= len(self.byFreqWordsToFreqInUse):
                    break

                currentWordFreqPair = self.byFreqWordsToFreqInUse[index]

                if self.WordIsInOutputData( currentWordFreqPair[0] ):
                    wordsWithinBounds.append( currentWordFreqPair[0] )
                    frequenciesWithinBounds.append( currentWordFreqPair[1] )
                else:
                    stopIndex += 1

            return (wordsWithinBounds, frequenciesWithinBounds)

    def CacheOrganizedWordFrequencyLists(self):
        self.byFreqWordsToFrequency.clear()
        self.byFreqWordsToFrequency.extend(sorted(self.wordsToFrequency.items(), key=lambda item: item[1], reverse=True))

        self.allLowerByFreqWordsToFreq.clear()
        self.allLowerByFreqWordsToFreq.extend(sorted(self.allLowerWordsToFrequency.items(), key=lambda item: item[1], reverse=True))

    def CountIndividualWordIntoCache(self, word: str):
        if word in self.wordsToFrequency:
            self.wordsToFrequency[word] += 1 # Add one more occurence
        else:
            self.wordsToFrequency.update({word : 1}) # Add first instance

        if word.lower() in self.allLowerWordsToFrequency:
            self.allLowerWordsToFrequency[word.lower()] += 1 # Add one more occurence
        else:
            self.allLowerWordsToFrequency.update({word.lower() : 1}) # Add first instance

    def CacheWordFrequencies(self):
        for i in range(len(self.currentTokenizedWords)):
            self.CountIndividualWordIntoCache(self.currentTokenizedWords[i])

    def CacheLinesIntoTokenizedWords(self, allFilelines):
        self.currentTokenizedWords.clear() # Create empty list that will be populated with the individual words
    
        for i in range(len(allFilelines)):
            line = allFilelines[i]

            line = str.translate(line, str.maketrans(editedOutPunctuation))
            line = str.split(line) # The line has been divied up into an array of the individual words

            for j in range(len(line)):
                self.currentTokenizedWords.append(line[j])

    def CacheTokenizedFileIntoBlacklist(self, tokenizedFile: list[str]):
        self.blacklist.clear()

        for i in range(len(tokenizedFile)):
            self.blacklist.append(tokenizedFile[i])

            self.allLowerBlacklist.append(tokenizedFile[i].lower())

cachedFiles: list[CachedFile] = []

def GetNextFileVersion(baseName):
    fileVersion = 0

    for file in cachedFiles:
        if file.fileName.startswith(baseName):
            fileVersion += 1

    return "" if fileVersion == 0 else str(fileVersion)

def CreateDefaultCachedFile(fileName):
    cachedFiles.append(CachedFile( fileName + GetNextFileVersion(fileName) ))

    return cachedFiles[len(cachedFiles) - 1]

def GetCachedFileByName(name):
    for file in cachedFiles:
        if file.fileName == name:
            return file
        
    return None

def TokenizeFileFromLines(allLines):
    tokenizedContent = []

    for i in range(len(allLines)):
        line = allLines[i]

        line = str.translate(line, str.maketrans(editedOutPunctuation))
        line = str.split(line) # The line has been divied up into an array of the individual words

        for j in range(len(line)):
            tokenizedContent.append(line[j])
    
    return tokenizedContent
