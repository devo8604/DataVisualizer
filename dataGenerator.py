# Python Modules
import random
import json
from datetime import timedelta, datetime, date


def dataGen(rData):
    """Control number that the deviation percentage is
    calculated from and empty dict Var"""
    CONTROL = 10
    randDate = (date.today() - (timedelta(days=100)))

    for x in range(100):
        randResult = random.randint(5, 15)
        randDate += (timedelta(days=1))
        deviationCalc = 100 * (abs((randResult - CONTROL)) / CONTROL)

        # Create the Datapoint "object" and appends it to the dict
        rData.update({"Build" + str(x): {"Result": randResult,
                                         "Date": datetime.strftime(randDate, '%Y-%m-%d'),
                                         "PercentDeviation": deviationCalc}})


def dataToJson(rData):
    "Sends the data to a JSON file"
    # Outputs objects to dataPoints.json file
    with open("dataPoints.json", "w") as outfile:
        json.dump(rData, outfile, indent=4)


def dataToDb():
    "Sends the data to a DB"
    print("Not Implemented yet")


def main():
    dataDict = {}

    dataGen(dataDict)
    dataToJson(dataDict)


if __name__ == '__main__':
    main()
