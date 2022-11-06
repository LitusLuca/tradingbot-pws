from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from datetime import date

file = input('data file: ')

try:
  cnx = mysql.connector.connect(user='Bator',password='Amber!0219',database='indexes')
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

if file == 'AEXdata.txt':
    add_date =("INSERT INTO `aex` (Date, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)")
elif file == 'Appleindex.csv':
    add_date =("INSERT INTO `apple` (Date, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)")


data = open(file).read()

data = data.split('\n')
x = 0
for daydata in data:
    if daydata == ' ':
        print('donald')
        continue
    daysplit = daydata.split(',')
    datum = daysplit[0]
    YMD = datum.split('-') 
    print(YMD)
    datum = date(int(YMD[0]),int(YMD[1]),int(YMD[2]))
    daydata = (datum , daysplit[1], daysplit[2], daysplit[3], daysplit[4], int(daysplit[5]) )
    cursor.execute(add_date, daydata)
    x= x + 1
    
cnx.commit()
print(x)
cursor.close()
cnx.close()
