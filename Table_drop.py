import mysql.connector
from mysql.connector import errorcode
from _env import password

DB_NAME = 'indexes'

what = str(input("drop what table? "))

try:
  cnx = mysql.connector.connect(user='Bator',password=password,database='indexes')
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  else:
    print(err)

if what == "all":
  cursor.execute("DROP TABLE `markets`")
  cursor.execute("DROP TABLE `indexes`")
  cursor.execute("DROP TABLE `stock_properties`")
  cursor.execute("DROP TABLE `aex`")
  cursor.execute("DROP TABLE `apple`")
  cursor.execute("DROP TABLE `meta`")
  cursor.execute("DROP TABLE `microsoft`")
  print('dropped all')
else:
  cursor.execute("DROP TABLE `{}`".format(what))
  print('dropped '+what)

cnx.commit()
cursor.close()
cnx.close()
