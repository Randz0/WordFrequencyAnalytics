from abc import ABC, abstractmethod
import IOReader
import DataParser
import Visualizer

class Command:
    def __init__(self):
        self.context_prop = None # The actual underlying value of the property
        self.validCommand = True

    # Sets the internal state of the command, assigned by the entire line
    @property
    def context(self):
        pass

    @abstractmethod
    def ActivateCommand(self):
        pass

class GetOcurrences(Command):
    @property
    def context(self):
        pass

    @context.setter
    def context(self, value):
        try:
            if value[5] == "c": # Not Case Sensitive, Default is case sensitive
                self.isCaseSensitive = False

            self.context_prop = value[7::] # Get the actual word
        except:
            self.validCommand = False # the feedback was unprocessable
    
    @context.getter
    def context(self):
        return self.context_prop
    
    def FindCaseSensitiveOcurrences(self):
        if not self.context in DataParser.Cached.defaultWordsToFrequency:
            print(0)

            return

        print(DataParser.Cached.defaultWordsToFrequency[self.context])

    def FindNonCaseSensitiveOcurrences(self):
        for key in DataParser.Cached.allLowerWordsToFrequency.keys():
            if key.lower() == self.context.lower():
                print(DataParser.Cached.allLowerWordsToFrequency[key])

                return

        print(0)

    # Returns 0 if the identifier doesn't exist
    def ActivateCommand(self):
        if self.isCaseSensitive:
            self.FindCaseSensitiveOcurrences()
        else:
            self.FindNonCaseSensitiveOcurrences()
            

    def __init__(self):
        super().__init__()

        self.isCaseSensitive = True

class OpenFile(Command):
    @property
    def context():
        pass

    @context.getter
    def context(self):
        return self.context_prop

    @context.setter
    def context(self, value):
        self.context_prop = value[5::]

    def ActivateCommand(self):
        try:
            textLines = IOReader.TryExtractTextLines(self.context)
            DataParser.currentTokenizedWords = DataParser.CacheTokenizedFileAsWords(textLines)
            
            DataParser.CacheWordFrequencies(DataParser.Cached.currentTokenizedWords)

            DataParser.CacheOrganizedWordFrequencyList(DataParser.Cached.defaultWordsToFrequency, DataParser.Cached.byFreqWordsToFrequency)
            DataParser.CacheOrganizedWordFrequencyList(DataParser.Cached.allLowerWordsToFrequency, DataParser.Cached.allLowerByFreqWordsToFreq)

            DataParser.Cached.currentPlotBounds = (0, len(DataParser.Cached.byFreqWordsToFrequency) - 1)
        except:
            print("Could not open requested file")
            return
        
        print("File opened sucessfully")

class PlotCurrentData(Command):
    @property
    def context(self):
        return self.context_prop
    
    @context.getter
    def context(self):
        return self.context_prop
    
    @context.setter
    def context(self, value):
        commandSettings = str.split(value) # Should be 2 long (plot, and Case Sensitive Flag)
        
        try:
            self.isCaseSensitive = commandSettings[1][0] == "C"

            return
        except ValueError:
            print("Number of Entries must be a positive number")
        except IndexError:
            print("Must Specify Correct # of Args")
        except Exception:
            pass # Will only print generic exception documentation

        self.validCommand = False

    def __init__(self):
        super().__init__()

        self.isCaseSensitive = True

    def ActivateCommand(self):
        try:
            Visualizer.LoadInGraphData(self.isCaseSensitive)
            Visualizer.RenderBarGraph()
        except Exception:
            print("Could not plot the data.")
            return
        
        print("Sucessfully graphed data")

class SetPlotBounds(Command):
    @property
    def context():
        pass

    @context.getter
    def context(self):
        return self.context_prop
    
    @context.setter
    def context(self, value):
        startStopIndexesStr = str.split(value)

        try:
            self.startStopIndexes = ( int(startStopIndexesStr[1]) - 1, int(startStopIndexesStr[2]) - 1 )

            return
        except IndexError:
            print("Invalid Command Args")
        except ValueError:
            print("Enter in Numbers for the Bounds")
        except Exception:
            pass

        self.validCommand = False
    
    def ActivateCommand(self):
        DataParser.Cached.currentPlotBounds = self.startStopIndexes

        print (f"Set Plot Bound Indexes To ({self.startStopIndexes[0]}, {self.startStopIndexes[1]})")

    def __init__(self):
        super().__init__()

        self.startStopIndexes = (0, 0)
        self.validCommand = True

# Returns None if the input matches no recognizable command, otherwise returns the command object
def RecieveNextCommand(consoleInput):
    outputCommand = None
    
    if str.startswith(consoleInput, "find"):
        outputCommand = GetOcurrences()
    elif str.startswith(consoleInput, "open"):
        outputCommand = OpenFile()
    elif str.startswith(consoleInput, "plot"):
        outputCommand = PlotCurrentData()
    elif str.startswith(consoleInput, "setBounds"):
        outputCommand = SetPlotBounds()
    else:
        return None
    
    outputCommand.context = consoleInput

    if not outputCommand.validCommand:
        print("Not Valid Command Syntax")

        return None
    
    return outputCommand
