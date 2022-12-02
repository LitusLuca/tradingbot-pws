from __future__ import print_function

from datetime import date

import mysql.connector
from mysql.connector import errorcode

from _env import password,user

file = input('data file: ')

try:
  cnx = mysql.connector.connect(user=user,password=password,database='indexes')
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

table_name= file.replace('.','\\')
table_name= table_name.split('\\')
table_name= table_name[1]


add_date =("INSERT INTO `{}` (Date, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)".format(table_name))


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

