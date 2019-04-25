import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import json

# Variable List
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

# Plot Builder
plt.plot(dateArr, deviationArr, 'r.')
plt.title("Deviation from actual expected value")
plt.ylabel("Percent Deviation")
plt.xlabel("Build Date")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot.png')
plt.show()

exit(0)
