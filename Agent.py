import random
from collections import deque
from statistics import mode

import numpy
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from os.path import exists


class TradingAgent:
    def __init__(self, state_size, action_size, gamma = 0.99, epsilon = 1.0, epsilonDeqay = 0.9999, epsilonMinimum = 0.05, safeFile = ""):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = gamma
        self.exploration = epsilon
        self.exploration_decay = epsilonDeqay
        self.exploration_min = epsilonMinimum
        self.learningrate = 0.001
        self.model = self._createModel()
        self.safefile = safeFile

        print("Hello, agent!")


    def _epsilonDeqay(self):
        if self.exploration > self.exploration_min:
            self.exploration *= self.exploration_decay

    def predictAction(self, state):
        self._epsilonDeqay()
        if random.random() < self.exploration:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state, verbose=0)[0]
        print(q_values)
        return numpy.argmax(q_values)

    def _createModel(self): 
        model = Sequential()
        model.add(Dense(32, input_dim=self.state_size, activation="relu"))
        model.add(Dense(16, activation="relu"))
        model.add(Dense(8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learningrate))
        return model
        
    def remember(self, state, action, reward, next, finished):
        self.memory.append((state,action,reward,next,finished))
    
    def trainMemories(self, traningSize):
        if len(self.memory) < traningSize:
            return
        traningBatch = random.sample(self.memory, traningSize)
        for state, action, reward, next, finished in traningBatch:
            targetQ = reward
            if not finished:
                qValues = self.model.predict(next, verbose=0)
                targetQ += self.gamma * numpy.amax(qValues[0])
            fullTargetQ = self.model.predict(state, verbose=0)
            fullTargetQ[0][action] = targetQ
            self.model.fit(state, fullTargetQ, epochs=1, verbose=0)

    def load(self):
        if exists(self.safefile):
            self.model.load_weights(self.safefile)
    
    def save(self):
        self.model.save_weights(self.safefile)
        print(self.exploration)
