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

# =============================================================================


def dataGen():
    """Generates Random Data"""
    CONTROL = 10
    randDate = (date.today() - (timedelta(days=100)))
    rData = {}

    # Generates 100 items
    for x in range(100):
        randResult = random.randint(5, 15)
        randDate += (timedelta(days=1))
        deviationCalc = 100 * (abs((randResult - CONTROL)) / CONTROL)

        # Create the Datapoint "object" and appends it to the dict
        rData.update({"Build" + str(x): {"Result": randResult,
                                         "Date": datetime.strftime(randDate, '%Y%m%d'),
                                         "PercentDeviation": deviationCalc}})

    return rData

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


def createDbTable(db):
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

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS testdata")
    cursor.execute(testDataTable)
    db.commit()

# =============================================================================


def insertTableData(db, rData):
    """Inserts data into the testData table"""

    # SQL Statement
    sql = "INSERT INTO testdata (`result`, `build_date`, `percent_deviation`) VALUES (%s, %s, %s)"

    cursor = db.cursor()
    for x in range(len(rData)):
        try:
            cursor.execute(sql, (rData["Build" +
                                       str(x)]["Result"],
                                 rData["Build" +
                                       str(x)]["Date"],
                                 rData["Build" + str(x)]["PercentDeviation"]))

            db.commit()
        except:
            print("Something doesn't feel right, rolling back the DB...")
            db.rollback()

# =============================================================================


def retrieveData(db):
    """Retrive all of the data from the table"""

    cursor = db.cursor()
    resultsDict = {}

    cursor.execute("SELECT * FROM testdata")
    row = cursor.fetchone()

    while row is not None:
        resultsDict.update({str(row[0]): {"Result": row[1],
                                          "Date": row[2],
                                          "PercentDeviation": row[3]}})
        row = cursor.fetchone()

    return resultsDict

# =============================================================================


def main():
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

        # Database Object
        dbinfo = pymysql.connect(dbHost, dbUser, dbUserPass, dbTable)

        genDict = dataGen()
        dataToJson(genDict)

        createDbTable(dbinfo)
        insertTableData(dbinfo, genDict)
        # dbDict = retrieveData(dbHost, dbUser, dbUserPass, dbTable)

        dbinfo.close()

# =============================================================================


if __name__ == '__main__':
    main()
