import datetime
import math

import mysql.connector
import numpy as np

from _env import password


class StockSimulation:
    def __init__(self, instrument, episodeLength, episodeStart) -> None:
        self.time = 0
        self.windowSize = 30
        self.inventory = []
        self.profit = 0.0
        self.instrument = instrument #TODO
        self.actionSpace = 3
        self.inputSpace = 40
        self.traningdata = self._getData(instrument, episodeStart, episodeLength)
        self.instrumentValue = 0
        #maybe sort traningdata


    def _getData(self, instrument, startDate, lenght):
        pass

    def reset(self):
        #TODO store results
        self.time = 0
        self.profit = 0
        self.inventory.clear()


        pass

    def getState(self):
        """set instrument value and format/return current state to the agent"""
        return []

    def action(self, action):
        reward = 0.0
        if action == 0:
            print("buying: ", self.instrument)
            self.inventory.append(self.instrumentValue)
        elif action == 1:
            print("selling: ", self.instrument)
            if self.inventory:
                reward = self.instrumentValue - self.inventory[0]
                self.inventory = self.inventory[1:]
            else:
                print("cant sell if you have nothing!!! BOZO-AGENT!!")
        elif action == 2:
            print("doing nothing")

        self.profit += reward
        next_state = []
        done = False
        self.time += 1
        return next_state, reward, done


if __name__ == "__main__":
    cnx = mysql.connector.connect(user='PWS',password=password, database='indexes')
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
