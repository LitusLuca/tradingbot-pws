from __future__ import print_function

from datetime import date

import mysql.connector
from mysql.connector import errorcode

from datetime import date

from _env import password,user

DB_NAME = 'indexes'

TABLES = {}

TABLES['Markets'] = (
    "CREATE TABLE `markets` ("
    "  `id` smallint(3) NOT NULL AUTO_INCREMENT,"
    "  `market_name` varchar(10) NOT NULL UNIQUE KEY,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['Indexes'] = (
    "CREATE TABLE `indexes` (" 
    "  `id` smallint(3) NOT NULL AUTO_INCREMENT,"
    "  `index_name` varchar(10) NOT NULL UNIQUE KEY,"
    "  `market_id` smallint(3) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


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

TABLES['Meta'] = (
    "CREATE TABLE `meta` (" 
    "  `Date` date NOT NULL,"
    "  `Open` decimal(11,6) NOT NULL,"
    "  `High` decimal(11,6) NOT NULL,"
    "  `Low` decimal(11,6) NOT NULL,"
    "  `Close` decimal(11,6) NOT NULL,"
    "  `Volume` int(11) NOT NULL,"
    "  PRIMARY KEY (`Date`)"
    ") ENGINE=InnoDB")

TABLES['Microsoft'] = (
    "CREATE TABLE `microsoft` (" 
    "  `Date` date NOT NULL,"
    "  `Open` decimal(11,6) NOT NULL,"
    "  `High` decimal(11,6) NOT NULL,"
    "  `Low` decimal(11,6) NOT NULL,"
    "  `Close` decimal(11,6) NOT NULL,"
    "  `Volume` int(11) NOT NULL,"
    "  PRIMARY KEY (`Date`)"
    ") ENGINE=InnoDB")

TABLES['Tesla'] = (
    "CREATE TABLE `tesla` (" 
    "  `Date` date NOT NULL,"
    "  `Open` decimal(11,6) NOT NULL,"
    "  `High` decimal(11,6) NOT NULL,"
    "  `Low` decimal(11,6) NOT NULL,"
    "  `Close` decimal(11,6) NOT NULL,"
    "  `Volume` int(11) NOT NULL,"
    "  PRIMARY KEY (`Date`)"
    ") ENGINE=InnoDB")

TABLES['TNX'] = (
    "CREATE TABLE `TNX` (" 
    "  `Date` date NOT NULL,"
    "  `Close` decimal(11,6) NOT NULL,"
    "  PRIMARY KEY (`Date`)"
    ") ENGINE=InnoDB")

try:

  cnx = mysql.connector.connect(user=user,password=password)
 
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

yesorno = input('add market and index info? ')
markets = {}
indexes = {}

markets['aex'] = ("INSERT INTO `markets` (market_name) VALUES ('aex')")
markets['nasdaq'] = ("INSERT INTO `markets` (market_name) VALUES ('nasdaq')")

indexes['aex'] = ("INSERT INTO `indexes` (index_name, market_id) VALUES ('aex','1')")
indexes['apple'] = ("INSERT INTO `indexes` (index_name, market_id) VALUES ('apple','2')")
indexes['meta'] = ("INSERT INTO `indexes` (index_name, market_id) VALUES ('meta','2')")
indexes['microsoft'] = ("INSERT INTO `indexes` (index_name, market_id) VALUES ('microsoft','2')")

if yesorno == 'yes':
    for market in markets:
        market_description = markets[market]
        try:
            cursor.execute(market_description)
        except:
            print('markets already added')
            break
    
    for index in indexes:
        index_description = indexes[index]
        try:
            cursor.execute(index_description)
        except:
            print('indexes already added')
            break
    print('done')



cnx.commit()
cursor.close()
cnx.close()
