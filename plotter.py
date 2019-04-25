# =============================================================================
#
# plotter.py is used to bring in JSON data from DB data and plot it using
# matplotlib.
#
# =============================================================================

import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import json

# Custom Modules
import dataGenerator

# Global Variable List
dataDict = {}
resultArr = []
deviationArr = []
dateArr = []

# =============================================================================


def getJsonData():
    """Read the JSON data into dataDict"""
    try:
        with open('dataPoints.json', 'r') as json_file:
            dataDict = json.load(json_file)
    except IOError as e:
        print(e)
        exit(1)

    # Iterates through dict and assigns the elements to the proper array for plot
    for x in range(len(dataDict)):
        resultArr.append(dataDict["Build"+str(x)]["Result"])
        # Must convert the date from string back to date
        dateArr.append(datetime.strptime(
            dataDict["Build"+str(x)]["Date"], '%Y%m%d'))
        deviationArr.append(dataDict["Build"+str(x)]["PercentDeviation"])

    # Dont need this anymore, set the mem free...
    dataDict.clear()

# =============================================================================


def getDataDb():
    """Calls the dataGenerator Module to get data from DB"""
    dataGenerator.retrieveData(dataDict)

    # Iterates through dict and assigns the elements to the proper array for plot
    for x in range(len(dataDict)):
        resultArr.append(dataDict[str(x+1)]["Result"])
        # Must convert the date from string back to date
        dateArr.append(datetime.strptime(
            dataDict[str(x+1)]["Date"], '%Y%m%d'))
        deviationArr.append(dataDict[str(x+1)]["PercentDeviation"])

# =============================================================================


def plotBuilder():
    """Builds the plot"""
    # Plot Builder
    plt.plot(dateArr, deviationArr, 'r.')
    plt.title("Deviation from actual expected value")
    plt.ylabel("Percent Deviation")
    plt.xlabel("Build Date")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plot.png')
    plt.show()

# =============================================================================


def main():
    getDataDb()
    plotBuilder()

# =============================================================================


if __name__ == '__main__':
    main()
