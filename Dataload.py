from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from datetime import date

DB_NAME = 'indexes'

TABLES = {}
file = input('data file: ')
name = input('index name: ')

TABLES[name] = (
    "CREATE TABLE `index` (" 
    "  `Date` date NOT NULL,"
    "  `Open` decimal(11,6) NOT NULL,"
    "  `High` decimal(11,6) NOT NULL,"
    "  `Low` decimal(11,6) NOT NULL,"
    "  `Close` decimal(11,6) NOT NULL,"
    "  `Adj_Close` decimal(11,6) NOT NULL,"
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

def create_database(cur):
    try:
        cur.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
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

add_date =("INSERT INTO `index` (Date, Open, High, Low, Close, Adj_Close, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s)")

data = open(file).read()

data = data.split('\n')
x = 0
for daydata in data:
    daysplit = daydata.split(',')
    datum = daysplit[0]
    YMD = datum.split('-') 
    datum = date(int(YMD[0]),int(YMD[1]),int(YMD[2]))
    daydata = (datum , daysplit[1], daysplit[2], daysplit[3], daysplit[4], daysplit[5], int(daysplit[6]) )
    cursor.execute(add_date, daydata)
    x= x + 1
    
cnx.commit()
print(x)
cursor.close()
cnx.close()

