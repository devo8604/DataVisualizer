# =============================================================================
#
# plotter.py is used to bring in JSON data from DB data and plot it using
# matplotlib.
#
# =============================================================================

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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


def getDataJson():
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
    try:
        with open('dbconfig.json') as config:
            data = json.load(config)
            dbHost = data["dbHost"]
            dbUser = data["dbUser"]
            dbUserPass = data["dbUserPass"]
            dbTable = data["dbTable"]
    except IOError as e:
        print(e)
    else:
        dataGenerator.retrieveData(
            dataDict, dbHost, dbUser, dbUserPass, dbTable)

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
    days = mdates.DayLocator()
    months = mdates.MonthLocator()
    timeFmt = mdates.DateFormatter('%b-%y')
    fig, ax = plt.subplots()

    plt.plot(dateArr, deviationArr, 'r.')
    plt.title("Deviation from actual expected value per build", fontsize=15)
    plt.ylabel("Percent Deviation", fontsize=15)
    plt.xlabel("Build Date", fontsize=15)
    plt.tight_layout()

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(timeFmt)
    ax.xaxis.set_minor_locator(days)

    plt.savefig('plot.png')
    plt.show()

# =============================================================================


def main():
    getDataJson()
    plotBuilder()

# =============================================================================


if __name__ == '__main__':
    main()
