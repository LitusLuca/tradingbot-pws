from datetime import datetime, timedelta
import math

import mysql.connector
import numpy as np

from _env import password, user


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


    def _getData(self, instrument, startDate, length):
        cnx = mysql.connector.connect(user=user,password=password, database='indexes')
        cursor = cnx.cursor()

        table = instrument

        dataquery = ("SELECT Date, Close FROM `{}`"
            "WHERE Date BETWEEN %s AND %s".format(table))

        first_date = datetime.strptime(startDate)
        last_date = first_date + timedelta(days=length)

        cursor.execute(dataquery, (first_date, last_date))

        alldata = []

        for (Date, Close) in cursor:
            print("On {:%d %b %Y} the data was: {}".format(
            Date, Close))
            alldata.append((Date,Close))
        
        marketquery = ("SELECT market_id FROM Indexes WHERE index_name = '{}'".format(table))
        cursor.execute(marketquery)
        for id in cursor:
            market_id = id[0]
        print(market_id)
        cursor.close
        indexquery = ("SELECT index_name FROM Indexes where market_id = {}".format(market_id))
        cursor.execute(indexquery)
        print("These indexes are in the same market:")
        for index in cursor:
            print(index[0])

        cursor.close()
        cnx.close()
        return alldata

    

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
