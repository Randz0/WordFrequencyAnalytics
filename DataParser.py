editedOutPunctuation = {"." : " ", "," : " ", "!" : " ", ":" : " ", ";" : " ", "?" : " ", "\n" : " "} # Dictionary used to filter out punctuation from the search result

class Cached:
    currentTokenizedWords = None

    defaultWordsToFrequency = {}
    allLowerWordsToFrequency = {}

    byFreqWordsToFrequency = []
    allLowerByFreqWordsToFreq = []

    currentPlotBounds = (0, 0)

# The input *allLines* should be a list containing all the lines of the input text file as strings
def CacheTokenizedFileAsWords(allFileLines):
    Cached.currentTokenizedWords = [] # Create empty list that will be populated with the individual words
    
    for i in range(len(allFileLines)):
        line = allFileLines[i]

        line = str.translate(line, str.maketrans(editedOutPunctuation))
        line = str.split(line) # The line has been divied up into an array of the individual words

        for j in range(len(line)):
            Cached.currentTokenizedWords.append(line[j])

def CountIndividualWordIntoCache(word):
    if word in Cached.defaultWordsToFrequency:
        Cached.defaultWordsToFrequency[word] += 1 # Add one more occurence
    else:
        Cached.defaultWordsToFrequency.update({word : 1}) # Add first instance

    if word.lower() in Cached.allLowerWordsToFrequency:
        Cached.allLowerWordsToFrequency[word.lower()] += 1 # Add one more occurence
    else:
        Cached.allLowerWordsToFrequency.update({word.lower() : 1}) # Add first instance

# expects the input to already be tokenized word by word
def CacheWordFrequencies(tokenizedInput):
    for i in range(len(tokenizedInput)): # Loop through every word
        CountIndividualWordIntoCache(tokenizedInput[i])

# Stores the word ocurrenences dictionary as a collection of tuples based on the frequency of each word from most to least ocurring
def CacheOrganizedWordFrequencyList(cachingFrom, cachingTo):
    cachingTo.clear()
    cachingTo.extend(sorted(cachingFrom.items(), key=lambda item: item[1], reverse=True))

# Returns a tuple of the words and their frequency only returning up to the depth most ocurring word 
def FetchWordsInFromPlotBounds(fetchingFrom):
    wordsWithinBounds = []
    frequenciesWithinBounds = []

    numberOfWordsToFetch = Cached.currentPlotBounds[1] - Cached.currentPlotBounds[0]

    for i in range(numberOfWordsToFetch):
        if i >= len(fetchingFrom):
            break

        wordsWithinBounds.append(fetchingFrom[i + Cached.currentPlotBounds[0]][0])
        frequenciesWithinBounds.append(fetchingFrom[i + Cached.currentPlotBounds[0]][1])

    return (wordsWithinBounds, frequenciesWithinBounds)
