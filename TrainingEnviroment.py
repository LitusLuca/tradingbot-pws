import numpy as np
import math
import datetime
import mysql.connector

class StockSimulation:
    def __init__(self) -> None:
        self.time = 0
        self.windowSize = 20
        self.inventory = []
        self.profit = 0.0
        self.stock = "TODO" #TODO
        pass
    def getTime(self) -> int:
        return self.time
    def _getData(self, stock: str, timeBegin: int, timeEnd: int):
        pass
    
    def _sigmoid(self, n: float):
        return 1 / (1 - math.exp(-n))

    def getState(self):
        data = self._getData(self, self.stock, self.time - self.windowSize, self.time)
        state = []
        for i_data in range(data):
            state.append(self._sigmoid(i_data))
        return np.array(data)

    def action(self, action: int):
        reward = 0

        next_state = []
        done = False
        return next_state, reward, done



cnx = mysql.connector.connect(user='Bator',password='', database='indexes')
cursor = cnx.cursor()

table = input('Table to insert into environment: ')

query = ("SELECT Date, Open, High, Low, Close, Volume FROM `{}`"
         "WHERE Date BETWEEN %s AND %s".format(table))

first_date = datetime.date.min
last_date = datetime.date.max

cursor.execute(query, (first_date, last_date))

for (Date, Open, High, Low, Close, Volume) in cursor:
    print("On {:%d %b %Y} the data was: {}, {}, {}, {}, {}".format(
    Date, Open, High, Low, Close, Volume))

cursor.close()
cnx.close()
