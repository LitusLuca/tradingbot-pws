from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from datetime import date

DB_NAME = 'indexes'

TABLES = {}


TABLES['AEX'] = (
    "CREATE TABLE `aex` (" 
    "  `Date` date NOT NULL,"
    "  `Open` decimal(11,6) NOT NULL,"
    "  `High` decimal(11,6) NOT NULL,"
    "  `Low` decimal(11,6) NOT NULL,"
    "  `Close` decimal(11,6) NOT NULL,"
    "  `Volume` int(11) NOT NULL,"
    "  PRIMARY KEY (`Date`)"
    ") ENGINE=InnoDB")

TABLES['Apple'] = (
    "CREATE TABLE `apple` (" 
    "  `Date` date NOT NULL,"
    "  `Open` decimal(11,6) NOT NULL,"
    "  `High` decimal(11,6) NOT NULL,"
    "  `Low` decimal(11,6) NOT NULL,"
    "  `Close` decimal(11,6) NOT NULL,"
    "  `Volume` int(11) NOT NULL,"
    "  PRIMARY KEY (`Date`)"
    ") ENGINE=InnoDB")

try:
  cnx = mysql.connector.connect(user='Bator',password='')
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
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

cursor.execute("DROP TABLE `apple`")

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
    
cnx.commit()
cursor.close()
cnx.close()

