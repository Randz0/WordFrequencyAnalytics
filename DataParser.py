translationTable = {"." : " ", "," : " ", "!" : " ", ":" : " ", ";" : " ", "?" : " ", "\n" : " "} # Dictionary used to filter out punctuation from the search result
ocurrenceTracker = {} # Dictionary used to track the amount of ocurrences of a word in the search file 

currentTokenizedWords = None

sortedOcurreces = None

# The input *allLines* should be a list containing all the lines of the input text file as strings
def TokenizeInputFileLinesToWords(allLines):
    splitVersion = [] # Create empty list that will be populated with the individual words
    
    for i in range(len(allLines)):
        line = allLines[i]

        line = str.translate(line, str.maketrans(translationTable))
        line = str.split(line) # The line has been divied up into an array of the individual words

        for j in range(len(line)):
            splitVersion.append(line[j])

    return splitVersion

# expects the input to already be tokenized word by word
def CountWordOcurrences(tokenizedInput):
    for i in range(len(tokenizedInput)): # Loop through every word
        if tokenizedInput[i] in ocurrenceTracker:
            ocurrenceTracker[tokenizedInput[i]] += 1 # Add one more occurence
        else:
            ocurrenceTracker.update({tokenizedInput[i] : 1}) # Add first instance

# Stores the word ocurrenences dictionary as a collection of tuples based on the frequency of each word from most to least ocurring
def CreateOrganizedWordOcurrences():
    global sortedOcurreces

    sortedOcurreces = sorted(ocurrenceTracker.items(), key=lambda item: item[1], reverse=True)

# Returns a tuple of the words and their frequency only returning up to the depth most ocurring word 
def FetchWordsUpToDepth(depth):
    wordsUpToDepth = []
    frequencyUpToDepth = []

    for i in range(depth):
        if i >= len(sortedOcurreces):
            break

        wordsUpToDepth.append(sortedOcurreces[i][0])
        frequencyUpToDepth.append(sortedOcurreces[i][1])

    return (wordsUpToDepth, frequencyUpToDepth)
