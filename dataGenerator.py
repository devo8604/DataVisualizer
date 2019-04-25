# Python Modules
import random
import json
from datetime import timedelta,datetime

#Control number that the deviation percentage is calculated from and empty dict Var
CONTROL = 10
dataDict = {}
randDate = (datetime.date(datetime.now()) - (timedelta(days=100)))

for x in range(100):
    randResult = random.randint(5,15)
    randDate += (timedelta(days=x)) 
    deviationCalc = 100 * (abs((randResult - CONTROL)) / CONTROL)

    #Create the Datapoint object and appends it to the dict
    dataDict.update({"Build" + str(x) : {"Result" : randResult, 
                                        "Date" : datetime.strftime(randDate, '%Y-%m-%d'), 
                                        "PercentDeviation" : deviationCalc}})


#Outputs objects to dataPoints.json file
with open("dataPoints.json", "w") as outfile:
        json.dump(dataDict, outfile, indent=4) 
