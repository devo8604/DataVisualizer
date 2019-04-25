# Python Modules
import random
import json
from datetime import timedelta, datetime, date
import pymysql


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
    """Sends the data to a JSON file"""
    # Outputs objects to dataPoints.json file
    with open("dataPoints.json", "w") as outfile:
        json.dump(rData, outfile, indent=4)


def createDbTable():
    """Sends the data to a DB

    To start mariaDB on Mac, use 'mysql.server start'
    To log in, type 'mysql -uroot'
    """

    testDataTable = """CREATE TABLE testdata(
        id INT NOT NULL AUTO_INCREMENT,
        result INT NOT NULL,
        build_date VARCHAR(10),
        percent_deviation FLOAT NOT NULL,
        PRIMARY KEY ( id ) )"""

    db = pymysql.connect("localhost", "dsmith", "QWer!@34", "dataplot")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS testdata")
    cursor.execute(testDataTable)

    db.close()


def insertTableData(rData):
    """Inserts data into the testData table"""

    db = pymysql.connect("localhost", "dsmith", "QWer!@34", "dataplot")
    cursor = db.cursor()

    for x in range(len(rData)):
        cursor.execute("""INSERT INTO testdata (result,
                        build_date,
                        percent_deviation) VALUES
                        ({result},
                        {build_date},
                        {percent_deviation})""".format(result=rData["Build" +
                                                                    str(x)]["Result"],
                                                                build_date=rData["Build"+str(x)]["Date"],
                                                                percent_deviation=rData["Build" + str(x)]["PercentDeviation"]))
    db.close()


def main():
    dataDict={}

    dataGen(dataDict)
    # dataToJson(dataDict)
    createDbTable()
    insertTableData(dataDict)


if __name__ == '__main__':
    main()
