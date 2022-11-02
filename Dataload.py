from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from datetime import date

DB_NAME = 'indexes'

TABLES = {}

TABLES['AEXdata'] = (
    "CREATE TABLE `aexdata` (" 
    "  `Date` date NOT NULL,"
    "  `Open` decimal(9,6) NOT NULL,"
    "  `High` decimal(9,6) NOT NULL,"
    "  `Low` decimal(9,6) NOT NULL,"
    "  `Close` decimal(9,6) NOT NULL,"
    "  `Adj Close` decimal(9,6) NOT NULL,"
    "  `Volume` int(11) NOT NULL,"
    "  PRIMARY KEY (`Date`)"
    ") ENGINE=InnoDB")

try:
  cnx = mysql.connector.connect(user='Bator',password='')
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
print("succes")

def create_database(cur):
    try:
        cur.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    print('dooo')
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

add_date =("INSERT INTO aexdata "
          "(Date, Open, High, Low, Close, Adj Close, Volume) "
          "VALUES (%s, %s, %s, %s, %s, %s, %s)")

data = open("AEXdata.txt").read()

data = data.split('\n')

for daydata in data:
    daysplit = daydata.split(',')
    datum = daysplit[0]
    YMD = datum.split('-') 
    date = date(int(YMD[0]),int(YMD[1]),int(YMD[2]))
    daydata = (date , float(daysplit[1]), float(daysplit[2]), float(daysplit[3]), float(daysplit[4]), float(daysplit[5]), int(daysplit[6]) )
    print(daydata)
    cursor.execute(add_date, daydata)
    print('doooooooooo')
    
cnx.commit()

cursor.close()
cnx.close()


