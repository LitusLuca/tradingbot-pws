from collections import deque
from statistics import mode
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import random
import numpy

class TradingAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(2000)
        self.gamma = 0.9
        self.exploration = 1.0
        self.exploration_decay = 0.99
        self.exploration_min = 0.05
        self.learningrate = 0.001
        self.model = self._createModel()

        print("Hello, agent!")
    def predict_action(self, state):
        if random.random() < self.exploration:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return numpy.argmax(q_values)

    def _createModel(self): 
        model = Sequential()
        model.add(Dense(32, input_dim=self.state_size, activation="relu"))
        model.add(Dense(16, activation="relu"))
        model.add(Dense(8, activation="relu"))
        model.add(Dense(self.action_size, activation="relu"))
        model.compile(loss="mse", optimize=Adam(lr=self.learningrate))
        return model


