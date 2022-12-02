import random
from collections import deque
from statistics import mode

import numpy
from keras.layers import Dense, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.models import Sequential
from keras.optimizers import Adam
from os.path import exists


class TradingAgent:
    def __init__(self, state_size, action_size, gamma = 0.99, epsilon = 1.0,
     epsilonDecay = 0.99, epsilonMinimum = 0.05, learningrate = 0.001, safeFile = ""):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = gamma
        self.exploration = epsilon
        self.exploration_decay = epsilonDecay
        self.exploration_min = epsilonMinimum
        self.learningrate = learningrate
        self.model = self._createModel()
        self.safefile = safeFile

        print("Hello, agent!")


    def epsilonDecay(self):
        if self.exploration > self.exploration_min:
            self.exploration *= self.exploration_decay

    def predictAction(self, state):
        if random.random() < self.exploration:
            return random.randrange(self.action_size)
        q_values = self.model.predict(numpy.reshape(state,[1, self.state_size[0], self.state_size[1]]), verbose=0)[0]
        print(q_values)
        return numpy.argmax(q_values)

    def _createModel(self): 
        model = Sequential()
        model.add(Conv1D(filters=64, kernel_size=2, activation="relu", input_shape=self.state_size))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
        #model.add(Dense(8, input_dim=self.state_size, activation="relu"))
        model.add(Dense(120, activation="relu"))
        model.add(Dense(60, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learningrate))
        return model
        
    def remember(self, memory):
        self.memory.append(memory)
    
    def trainMemories(self, trainingSize):
        if len(self.memory) < trainingSize:
            return
        trainingBatch = numpy.array(random.sample(self.memory, trainingSize))
        trainingBatch = numpy.swapaxes(trainingBatch,0,1)
        x_train = numpy.array(list(trainingBatch[0]), dtype=numpy.float32).reshape([trainingSize, self.state_size[0], self.state_size[1]])
        y_train = self.model.predict(x_train, verbose=0)
        rewards = trainingBatch[2]
        nextQ = numpy.amax(self.model.predict(numpy.array(list(trainingBatch[3]), dtype=numpy.float32).reshape([trainingSize, self.state_size[0], self.state_size[1]]), verbose=0), axis=1)
        targetQ = rewards + self.gamma*nextQ*(-1*(trainingBatch[4])+1)

        for i in range(len(y_train)):
            y_train[i][trainingBatch[1][i]] = targetQ[i]
        
        self.model.fit(x_train, y_train, batch_size=10, epochs=1, verbose=0)

    def load(self):
        if exists(self.safefile):
            self.model.load_weights(self.safefile)
    
    def save(self):
        self.model.save_weights(self.safefile)
