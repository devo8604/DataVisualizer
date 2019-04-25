import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json

dataDict = {}

resultArr = []
deviationArr = []
dateArr = []

# Read the JSON data
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
    dateArr.append(datetime.strptime(dataDict["Build"+str(x)]["Date"], '%Y-%m-%d'))
    deviationArr.append(dataDict["Build"+str(x)]["PercentDeviation"])

# Dont need this anymore, set the mem free...
dataDict.clear()

convertedDates = mdates.datestr2num(dateArr)
plt.plot(deviationArr, dateArr, 'r.')

plt.title("Deviation from actual expected value")
plt.xlabel("Percent Deviation")
plt.ylabel("Build Date")
plt.savefig('plot.png')
plt.show()

exit(0)
