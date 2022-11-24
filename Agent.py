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


    def epsilonDeqay(self):
        if self.exploration > self.exploration_min:
            self.exploration *= self.exploration_decay

    def predictAction(self, state):
        if random.random() < self.exploration:
            return random.randrange(self.action_size)
        q_values = self.model.predict(numpy.reshape(state,[1, self.state_size]), verbose=0)[0]
        print(q_values)
        return numpy.argmax(q_values)

    def _createModel(self): 
        model = Sequential()
        model.add(Dense(8, input_dim=self.state_size, activation="relu"))
        model.add(Dense(8, activation="relu"))
        model.add(Dense(8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learningrate))
        return model
        
    def remember(self, memory):
        self.memory.append(memory)
    
    def trainMemories(self, traningSize):
        if len(self.memory) < traningSize:
            return
        traningBatch = numpy.array(random.sample(self.memory, traningSize))
        traningBatch = numpy.swapaxes(traningBatch,0,1)
        x_train = numpy.array(list(traningBatch[0]), dtype=numpy.float32)
        y_train = self.model.predict(x_train, verbose=0)
        rewards = traningBatch[2]
        nextQ = numpy.amax(self.model.predict(numpy.array(list(traningBatch[3]), dtype=numpy.float32), verbose=0), axis=1)
        targetQ = rewards + nextQ*(-1*(traningBatch[4]))

        for i in range(len(y_train)):
            y_train[i][traningBatch[1][i]] = targetQ[i]
        


        # x_train = [state for state, _,_,_,_ in traningBatch]
        # y_train = [reward ]
        # for state, action, reward, next, finished in traningBatch:
        #     targetQ = reward
        #     if not finished:
        #         qValues = self.model.predict(next, verbose=0)
        #         targetQ += self.gamma * numpy.amax(qValues[0])
        #     fullTargetQ = self.model.predict(state, verbose=0)
        #     fullTargetQ[0][action] = targetQ
        #     x_train.append(state[0])
        #     y_train.append(fullTargetQ[0])
        #     print(x_train.shape, y_train.shape)
        self.model.fit(x_train, y_train, batch_size=10, epochs=1, verbose=0)
        

        #for state, action, reward, next, finished in traningBatch:
        #    targetQ = reward
        #    if not finished:
        #        qValues = self.model.predict(next, verbose=0)
        #        targetQ += self.gamma * numpy.amax(qValues[0])
        #    fullTargetQ = self.model.predict(state, verbose=0)
        #    fullTargetQ[0][action] = targetQ
        #    self.model.fit(state, fullTargetQ, epochs=1, verbose=0)

    def load(self):
        if exists(self.safefile):
            self.model.load_weights(self.safefile)
    
    def save(self):
        self.model.save_weights(self.safefile)
