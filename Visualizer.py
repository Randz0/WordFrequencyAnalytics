import matplotlib.pyplot as plt
import numpy as np
import DataParser

# Load in the variables that will be used to contruct the output graph
figure = None
axes = None

def OnYLimChange():
    yLimits = axes.get_ylim()
    yLimitsHeight = yLimits[1] - yLimits[0]

    if yLimits[0] < 0:
        axes.set_ylim(0, yLimitsHeight)

def LoadInGraphData(numberOfWords):
    global figure, axes

    figure, axes = plt.subplots()

    data = DataParser.FetchWordsUpToDepth(numberOfWords)

    axes.bar(data[0], data[1], width=0.4, align="center")

    axes.set_title("Ocurrences Of Each Word")
    
    axes.set_xlabel("Times Repeated")
    axes.set_ylabel("Words")

    axes.callbacks.connect("ylim_changed", lambda evt: OnYLimChange())

def RenderBarGraph():
    plt.show()