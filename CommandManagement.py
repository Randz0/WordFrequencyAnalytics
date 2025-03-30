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
        if not self.context in DataParser.ocurrenceTracker:
            print(0)

            return

        print(DataParser.ocurrenceTracker[self.context])

    def FindNonCaseSensitiveOcurrences(self):
        for key in DataParser.ocurrenceTracker.keys():
            if key.lower() == self.context.lower():
                print(DataParser.ocurrenceTracker[key])

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
            DataParser.currentTokenizedWords = DataParser.TokenizeInputFileLinesToWords(textLines)
            
            DataParser.CountWordOcurrences(DataParser.currentTokenizedWords)
            DataParser.CreateOrganizedWordOcurrences()
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
        self.context_prop = value[5::]

    def ActivateCommand(self):
        try:
            Visualizer.LoadInGraphData(int(self.context))
            Visualizer.RenderBarGraph()
        except ValueError:
            print("Could Not Recognize The Number of Entries Requested as a Number")
            return
        except Exception as e:
            print("Could not plot the data.")
            return
        
        print("Sucessfully graphed data")

# Returns None if the input matches no recognizable command, otherwise returns the command object
def RecieveNextCommand(consoleInput):
    outputCommand = None
    
    if str.startswith(consoleInput, "find"):
        outputCommand = GetOcurrences()
    elif str.startswith(consoleInput, "open"):
        outputCommand = OpenFile()
    elif str.startswith(consoleInput, "plot"):
        outputCommand = PlotCurrentData()
    else:
        return None
    
    outputCommand.context = consoleInput

    if not outputCommand.validCommand:
        print("Not Valid Command Syntax")

        return None
    
    return outputCommand