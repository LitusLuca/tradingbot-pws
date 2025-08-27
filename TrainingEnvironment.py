import math
from datetime import datetime, timedelta

import mysql.connector
import numpy
from sklearn.preprocessing import StandardScaler, MinMaxScaler


from _env import password, user
from openpyxl import Workbook, load_workbook
from os.path import exists


class StockSimulation:
    def __init__(self, instrument, timeSpan, episodeStart, results):
        self.time = 0
        self.windowSize = 10
        self.inventory = []
        self.invested = 0.0
        self.profit = 0.0
        self.instrument = instrument #TODO
        self.actionSpace = 3
        self.features = 4
        #self.inputSpace = self.windowSize * 5 + 3 #+3: invested profit and inventorie lenght
        self.inputSpace = [self.windowSize, self.features]
        self.trainingdata = self._getData(instrument, episodeStart-timedelta(days=self.windowSize), timeSpan)
        self.instrumentValue = self.trainingdata[self.time][4]
        print(self.instrumentValue)

    #values for storing results
        if exists(results):
            self.wb = load_workbook(results)
        else:
            self.wb = Workbook()
        self.ws = self.wb.active
        self.specialparameter = 0.0
        self.specialparameterIterator = 0
        self.episode = 1
        self.ws["A1"] = "episode \\ parameter"
        self.ws["B1"] = self.specialparameter
        self.wb.save(results)
        self.resultsfile = results
        self.epsilon = 0
        self.startDate = episodeStart


    def _getData(self, instrument, startDate, length):
        cnx = mysql.connector.connect(user=user,password=password, database='indexes')
        cursor = cnx.cursor()

        table = instrument

        dataquery = (
            "SELECT i.Date, i.Open, i.High, i.Low, i.Close, i.Volume FROM `{}` AS i "
            "WHERE i.date BETWEEN %s AND %s"
        ).format(table)

        first_date = startDate
        last_date = first_date + timedelta(days=length)

        cursor.execute(dataquery, (first_date, last_date))

        alldata = []

        for (Date, Open, High, Low, Close, Volume) in cursor:
            #print("On {:%d %b %Y} the data was: {}".format(Date, Close))
            alldata.append([Date,float(Open), float(High), float(Low), float(Close), int(Volume)])
            #print(alldata, numpy.shape(alldata))
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
        alldata = numpy.array(alldata, dtype=object)
        print(alldata, numpy.shape(alldata))
        return alldata

    def getEpisodeLength(self):
        return len(self.trainingdata) - self.windowSize - 1

    def reset(self, specialParameter = 0.0, hardReset = False):
        #TODO store results
        
        self.ws.cell(row=self.episode + 1, column= self.specialparameterIterator + 2, value= self.profit)
        self.ws.cell(row=self.episode + 1, column=1, value=self.episode)
        self.ws.cell(row=self.episode + 1, column=3, value=self.epsilon)
        self.ws.cell(row=self.episode + 1, column=4, value=self.startDate)
        if hardReset:
            self.specialparameterIterator += 1
            self.specialparameter = specialParameter
            self.episode = 1
            self.ws.cell(row=1, column= self.specialparameterIterator + 2, value=specialParameter)
        
        self.wb.save(self.resultsfile)
        self.episode += 1
        self.time = 0
        self.profit = 0.0
        self.invested = 0.0
        self.inventory.clear()

    def getState(self):
        """set instrument value and format/return current state to the agent"""
        scaler = StandardScaler()
        idx = self.time + self.windowSize
        if idx >= len(self.trainingdata):
            return None
            
        row = self.trainingdata[idx]
        yester = self.instrumentValue
        self.instrumentValue = float(row[4])
        # Get window of numeric data 
        data_window = self.trainingdata[self.time:idx]
        
        #numeric_data = numpy.array([[float(r[1]),float(r[2]),float(r[3]),float(r[4]),float(r[5])] for r in data_window], dtype="float32")
        #numeric_data = scaler.fit_transform(numeric_data)

        #if len(self.inventory) > 0:
        #    sellprofit = numeric_data[:, 4] - self.inventory[0]
        #else:
        #    sellprofit = numpy.zeros(self.windowSize, dtype="float32")
        #sellprofit = sellprofit.reshape(-1, 1)    
        Close = numpy.array([[float(data_window[i][4])] for i in range(self.windowSize)], dtype="float32")
        Close = scaler.fit_transform(Close)
        Close = Close.reshape(-1, 1)

        log_returns = numpy.array([[math.log(float(data_window[i+1][4]) / float(data_window[i][4])) if i < self.windowSize - 1 else 0.0] for i in range(self.windowSize)], dtype="float32")
        log_returns = scaler.fit_transform(log_returns)
        log_returns = log_returns.reshape(-1, 1)

        range_ratio = numpy.array([[(float(data_window[i][2])- float(data_window[i][3])) / float(data_window[i][1])] for i in range(self.windowSize)], dtype="float32")
        range_ratio = range_ratio.reshape(-1, 1)

        vol = numpy.array([data_window[:, 5]], dtype="float32")
        vol = scaler.fit_transform(vol)
        vol = vol.reshape(-1, 1)

        data = numpy.hstack([Close, log_returns, range_ratio, vol])
        return data

    def action(self, action):
        reward = 0.0
        if action == 0:
            self.inventory.append(self.instrumentValue)
            self.invested += self.instrumentValue
        elif action == 1 and self.inventory:
            self.invested -= self.inventory[0]
            reward = self.instrumentValue - self.inventory[0]
            self.inventory = self.inventory[1:]

        self.profit += reward
        print("On t={} the profit is: {:.2f}".format(self.time, self.profit))
        self.time += 1

        if self.time + self.windowSize >= len(self.trainingdata):
            done = True
            next_state = None
        else:
            done = False
            next_state = self.getState()
        
        return next_state, reward, done
