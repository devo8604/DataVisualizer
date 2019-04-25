# =============================================================================
#
# dataGenerator.py is used to generate a random data set to be stored as JSON
# or in a DB.
#
# =============================================================================

# Python Modules
import random
import json
from datetime import timedelta, datetime, date
import pymysql

# Global Variables for DB access
dbHost = "localhost"
dbUSer = "dsmith"
dbUserPass = "QWer!@34"
dbTable = "dataPlot"

# =============================================================================


def dataGen(rData):
    """Generates Random Data"""
    CONTROL = 10
    randDate = (date.today() - (timedelta(days=100)))

    # Generates 100 items
    for x in range(100):
        randResult = random.randint(5, 15)
        randDate += (timedelta(days=1))
        deviationCalc = 100 * (abs((randResult - CONTROL)) / CONTROL)

        # Create the Datapoint "object" and appends it to the dict
        rData.update({"Build" + str(x): {"Result": randResult,
                                         "Date": datetime.strftime(randDate, '%Y%m%d'),
                                         "PercentDeviation": deviationCalc}})

# =============================================================================


def dataToJson(rData):
    """Sends the data to a JSON file"""
    try:
        with open("dataPoints.json", "w") as outfile:
            json.dump(rData, outfile, indent=4)
    except IOError as e:
        print(e)
        exit(1)

# =============================================================================


def createDbTable():
    """Sends the data to a DB

    To start mariaDB on Mac, use 'mysql.server start'
    To log in, type 'mysql -uroot'
    """

    testDataTable = """CREATE TABLE testdata(
        id INT NOT NULL AUTO_INCREMENT,
        result INT NOT NULL,
        build_date TEXT,
        percent_deviation FLOAT NOT NULL,
        PRIMARY KEY ( id ) )"""
    try:
        db = pymysql.connect(dbHost, dbUSer, dbUserPass, dbTable)
    except:
        print("Did you remember to start the DB service?")
    else:
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS testdata")
        cursor.execute(testDataTable)
        db.commit()
        db.close()

# =============================================================================


def insertTableData(rData):
    """Inserts data into the testData table"""

    try:
        db = pymysql.connect(dbHost, dbUSer, dbUserPass, dbTable)
    except:
        print("Did you remember to start the DB service?")

        cursor = db.cursor()
    for x in range(len(rData)):
        try:
            cursor.execute("""INSERT INTO testdata (result,
                                build_date,
                                percent_deviation) VALUES
                                ({result},
                                {build_date},
                                {percent_deviation})""".format(result=rData["Build" +
                                                                            str(x)]["Result"],
                                                               build_date=rData["Build" +
                                                                                str(x)]["Date"],
                                                               percent_deviation=rData["Build" + str(x)]["PercentDeviation"]))
            db.commit()

        except:
            print("Something doesn't feel right, rolling back the DB...")
            db.rollback()

    db.close()

# =============================================================================


def retrieveData(resultsDict):
    """Retrive all of the data from the table"""
    db = pymysql.connect(dbHost, dbUSer, dbUserPass, dbTable)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM testdata")
    row = cursor.fetchone()

    while row is not None:
        resultsDict.update({str(row[0]): {"Result": row[1],
                                          "Date": row[2],
                                          "PercentDeviation": row[3]}})
        row = cursor.fetchone()

    db.close()

# =============================================================================


def main():
    dataDict = {}

    dataGen(dataDict)
    dataToJson(dataDict)
    createDbTable()
    insertTableData(dataDict)
    retrieveData(dataDict)
    print(dataDict)

# =============================================================================


if __name__ == '__main__':
    main()
