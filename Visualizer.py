import matplotlib.pyplot as plt
import DataParser

# Load in the variables that will be used to contruct the output graph, leftover from the matplotlib framework
figure = None
axes = None

def OnYLimChange():
    yLimits = axes.get_ylim()
    yLimitsHeight = yLimits[1] - yLimits[0]

    if yLimits[0] < 0:
        axes.set_ylim(0, yLimitsHeight)

def SetBarGraphVisualStyle(axes):
    axes.set_title("Appearences Of Each Word")
    
    axes.set_xlabel("Words")
    axes.set_ylabel("Times Repeated")

    axes.callbacks.connect("ylim_changed", lambda evt: OnYLimChange())

def LoadInGraphData(cachedFile):
    global figure, axes

    figure, axes = plt.subplots()
    
    data = cachedFile.FetchWordsToFrequencies()

    axes.bar(data[0], data[1], width=0.6, align="center")

    SetBarGraphVisualStyle(axes)
    
def RenderBarGraph():
    plt.show()
