import IOReader
import DataParser
import Visualizer

class Command:
    helpInformation = "Empty Command, Does Nothing..."

    def __init__(self):
        self.validCommand = True

    def TryAbsorbContext(self, tokenizedContext):
        pass

    @property
    def context(self): # The setter's in particualar of this variable allow for data to be stored from the cmd line args
        pass

    def ActivateCommand(self):
        pass

    def TryActivateCommand(self):
        try:
            self.ActivateCommand()
        except:
            print ("Command Failed")

class GetOcurrences(Command):
    helpInformation = "Finds Number of Ocurrences of a word in a certain file. Expected Format: find (case sensitive) (savedFilename)"

    @property
    def context(self):
        pass

    def TryAbsorbContext(self, tokenizedContext):
        self.isCaseSensitive = tokenizedContext[1] == "C"

        self.wordSearchingFor = tokenizedContext[2]

        self.cachedFilename = tokenizedContext[3]
        
    @context.setter
    def context(self, value):
        try:
            self.TryAbsorbContext(value)

            return
        except IndexError:
            print("Command must have correct # of Args")

        self.validCommand = False # the feedback was unprocessable
    
    @context.getter
    def context(self):
        return self.wordSearchingFor

    def ActivateCommand(self):
        cachedFile = DataParser.GetCachedFileByName(self.cachedFilename)

        print( cachedFile.GetAppearencesOfWord(self.wordSearchingFor) )

    # Returns 0 if the identifier doesn't exist
    def TryActivateCommand(self):
        self.ActivateCommand()
            

    def __init__(self):
        super().__init__()

        self.isCaseSensitive: bool = True

        self.cachedFilename: str = None
        self.wordSearchingFor: str = None

class OpenFile(Command):
    helpInformation = "Opens a file for processing by the system. Expected format: open (file path) \n Optionally - as (saved filename)"

    @property
    def context():
        pass

    @context.getter
    def context(self):
        return self.filepath

    def TryAbsorbContext(self, tokenizedContext): # Expected Format: open {filename} as (optional) {saved filename} (default saved filename is the text file name)
        self.filepath = tokenizedContext[1]

        if len(tokenizedContext) >= 4:
            self.savedFilename = tokenizedContext[3]
        else:
            self.savedFilename = self.filepath

    @context.setter
    def context(self, value):
        try:
            self.TryAbsorbContext(value)
        except IndexError:
            print ("Must Contain Correct Number of Args")

    def TryActivateCommand(self):
        try:
            self.ActivateCommand()
        except:
            print("Could not open requested file")
            return
        
        print("File opened sucessfully")

    def ActivateCommand(self):
        textLines = IOReader.TryExtractTextLines(self.filepath)

        cachedFile = DataParser.CreateDefaultCachedFile(self.savedFilename)

        cachedFile.CacheLinesIntoTokenizedWords(textLines)
        cachedFile.CacheWordFrequencies()

        cachedFile.CacheOrganizedWordFrequencyLists()

        cachedFile.plotBounds = (0, len(cachedFile.byFreqWordsToFrequency) - 1)

    def __init__(self):
        super().__init__()

        self.filepath = None
        self.savedFilename = None

class RenameFile(Command):
    helpInformation = "Renames a file in the system. Expected format rename (old savedFilename) (new savedFilename)"

    def __init__(self):
        super().__init__()

        self.newName = None
        self.oldName = None

    @property
    def context(self):
        pass

    @context.getter
    def context(self):
        return self.newName

    def TryAbsorbContext(self, tokenizedContext):
        self.oldName = tokenizedContext[1]
        self.newName = tokenizedContext[2]

    @context.setter
    def context(self, value):
        try:
            self.TryAbsorbContext(value)

            return
        except:
            print ("Input Correct Number of Args")

        self.validCommand = False

    def ActivateCommand(self):
        cachedFile = DataParser.GetCachedFileByName(self.oldName)
        cachedFile.fileName = self.newName

    def TryActivateCommand(self):
        try:
            self.ActivateCommand()
        except:
            print ("Could not set new file name in system")
            return
        
        print (f"Able to change {self.oldName} to {self.newName}")

class PlotCurrentData(Command):
    helpInformation = "Plots information from a saved file using its stored properties (I.E. black/whitelist and what not). \n \
    Expected format: plot (case sensitive) (savedFilename)"

    @property
    def context(self):
        pass
    
    @context.getter
    def context(self):
        return self.validCommand
    
    def TryAbsorbContext(self, tokenizedContext):
        self.isCaseSensitive = tokenizedContext[1] == "C"

        self.cachedFilename = tokenizedContext[2]

    @context.setter
    def context(self, value):
        try:
            self.TryAbsorbContext(value)

            return
        except IndexError:
            print("Must Specify Correct # of Args")

        self.validCommand = False

    def __init__(self):
        super().__init__()

        self.isCaseSensitive = True
        self.cachedFilename = None

    def TryActivateCommand(self):
        try:
            self.ActivateCommand()
        except:
            print("Could not plot the data.")
            return
        
        print("Sucessfully graphed data")

    def ActivateCommand(self):
        cachedFile = DataParser.GetCachedFileByName(self.cachedFilename)
        cachedFile.isCaseSensitive = self.isCaseSensitive

        Visualizer.LoadInGraphData(cachedFile)
        Visualizer.RenderBarGraph()

class SetPlotBounds(Command):
    helpInformation = "Sets the bounds for graphed data by frequency for the given file. Expected format: setBounds (lower bound) (upper bound) (savedFilename)"

    @property
    def context():
        pass

    @context.getter
    def context(self):
        return self.startStopIndexes
    
    def TryAbsorbContext(self, tokenizedContext):
        self.startStopIndexes = ( int(tokenizedContext[1]) - 1, int(tokenizedContext[2]) - 1 )

        self.filename = tokenizedContext[3]

    @context.setter
    def context(self, value):
        try:
            self.TryAbsorbContext(value)

            return
        except IndexError:
            print("Must Set Correct Number of Command Args")
        except ValueError:
            print("Enter in Numbers for the Bounds")

        self.validCommand = False
    
    def TryActivateCommand(self):
        try:
            self.ActivateCommand()
        except:
            print ("Failed to set plot indexes")

    def ActivateCommand(self):
        cachedFile = DataParser.GetCachedFileByName(self.filename)
        cachedFile.plotBounds = self.startStopIndexes

        print (f"Set Plot Bound Indexes To ({self.startStopIndexes[0]}, {self.startStopIndexes[1]})")

    def __init__(self):
        super().__init__()

        self.startStopIndexes = (0, 0)
        self.filename = None

        self.validCommand = True

class SetBlacklist(Command):
    helpInformation = "nothing"

    @property
    def context():
        pass

    @context.getter
    def context(self):
        pass
    
    def TryAbsorbContext(self, tokenizedContext):
        self.filepath = tokenizedContext[1]
        self.cachedFilename = tokenizedContext[2]

    @context.setter
    def context(self, value):
        try:
            self.TryAbsorbContext(value)
        except IndexError:
            print("Enter Correct # Of Args")

    def __init__(self):
        super().__init__()

        self.filepath = None
        self.cachedFilename = None

    def ActivateCommand(self):
        cachedFile = DataParser.GetCachedFileByName(self.cachedFilename)

        tokenizedFile = []

        if self.filepath != "no-list":
            allLines = IOReader.TryExtractTextLines(self.filepath)
            tokenizedFile = DataParser.TokenizeFileFromLines(allLines)

        cachedFile.CacheTokenizedFileIntoBlacklist(tokenizedFile)

    def TryActivateCommand(self):
        try:
            self.ActivateCommand()
        except:
            print("Could not set blacklist")

            return

        print (f"Set Blacklist from {self.filepath}")

class SetWhitelist(Command):
    helpInformation = ""

    @property
    def context(self):
        pass

    @context.getter
    def context(self):
        return self.filepath

    def TryAbsorbContext(self, tokenizedContext):
        self.filepath = tokenizedContext[1]
        self.filename = tokenizedContext[2]

    @context.setter
    def context(self, value):
        try:
            self.TryAbsorbContext(value)
        except IndexError:
            print ("Unable to set whitelist. Incorrect Number of args")

            return

    def ActivateCommand(self):
        cachedFile = DataParser.GetCachedFileByName(self.filename)

        tokenizedFile = []

        if self.filepath != "no-list":
            fileLines = IOReader.TryExtractTextLines(self.filepath)
            tokenizedFile = DataParser.TokenizeFileFromLines(fileLines)
        
        cachedFile.CacheTokenizedFileIntoWhitelist(tokenizedFile)

    def TryActivateCommand(self):
        try:
            self.ActivateCommand()
        except:
            print("Unable to set whitelist.")

            return
        
        print ("Sucessfully set whitelist")

    def __init__(self):
        super().__init__()

        self.filepath = None
        self.filename = None

commandImplementations = { "find" : GetOcurrences,
                       "open" : OpenFile,
                       "plot" : PlotCurrentData,
                       "setBounds" : SetPlotBounds,
                       "setBlacklist" : SetBlacklist,
                       "setWhitelist" : SetWhitelist,
                       "rename" : RenameFile }

class GetHelpInformation(Command):
    @property
    def context(self):
        pass

    @context.setter
    def context(self, value):
        pass

    def TryActivateCommand(self):
        for commandName in commandImplementations.keys():
            print ( f"{commandName} - {commandImplementations[commandName].helpInformation} \n" )

def AddHelpMenu():
    commandImplementations.update( {"help" : GetHelpInformation } )

def RecieveNextCommand(consoleInput):
    tokenizedCommand = str.split(consoleInput)

    if not (len(tokenizedCommand) > 0 and tokenizedCommand[0] in commandImplementations.keys()):
        return Command()
    
    outputCommand = commandImplementations[tokenizedCommand[0]]()
    outputCommand.context = tokenizedCommand

    if not outputCommand.validCommand:
        print("Not Valid Command Syntax")

        return Command()
    
    return outputCommand
