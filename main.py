from datetime import date, timedelta

import numpy

from Agent import TradingAgent
from TrainingEnvironment import StockSimulation


def SimpleTraining(instrument ,episodes, timeSpan, episodeStartDate, iteration):
    environnment = StockSimulation(instrument, timeSpan, episodeStartDate, results="./results/simple-{}-{}.xlsx".format(instrument, iteration))
    agent = TradingAgent(environnment.inputSpace, environnment.actionSpace, safeFile="./models/simple-{}-{}.h5".format(instrument, iteration), epsilonDeqay=0.95)
    agent.load()

    for E in range(episodes):
        print("start episode: {:d}/{:d}, exploration: {:.2f}".format(E+1, episodes, agent.exploration))
        
        state = environnment.getState()
        print(state)
        agent.epsilonDecay()
        for t in range(environnment.getEpisodeLength()):
            action = agent.predictAction(state)
            nextState, reward, finished = environment.action(action)
            agent.remember(numpy.array([state, action, reward, nextState, finished], dtype=object))
            state = nextState
            if finished:
                break
            agent.trainMemories(200)
            if t % 50 == 0:
                agent.save()
        print("total profit: {:.2f}".format(environment.profit))
        environment.reset()

def randomDate(start: date, end: date):
    return start + numpy.random.random() * (end - start)

def ChangingTraining(instrument, episodes, episodeTimeSpan, minDate, maxDate, iteration):
    episodeStartDate = randomDate(minDate, maxDate)
    environment = StockSimulation(instrument, episodeTimeSpan, episodeStartDate, results="./results/changing-{}-{}.xlsx".format(instrument, iteration))
    agent = TradingAgent(environment.inputSpace, environment.actionSpace, safeFile="./models/changing-{}-{}.h5".format(instrument, iteration), epsilonDecay=0.9, gamma=0.9, epsilonMinimum=0.1, epsilon=0.5)
    agent.load()
    for E in range(episodes):
        print("start episode: {:d}/{:d}, exploration: {:.2f}".format(E+1, episodes, agent.exploration))
        print("--------------------\n")

        agent.epsilonDecay()
        environment.epsilon = agent.exploration

        state = environment.getState()
        for t in range(environment.getEpisodeLength()):
            action = agent.predictAction(state)
            nextState, reward, finished = environment.action(action)
            agent.remember(numpy.array([state, action, reward, nextState, finished], dtype=object))
            state = nextState
            if finished:
                break
            agent.trainMemories(200)
            if t % 50 == 0:
                agent.save()
        print("total profit: {:.2f}".format(environment.profit))
        environment.reset()
        print("----------------")
        episodeStartDate = randomDate(minDate, maxDate)
        print(episodeStartDate)
        environment.trainingdata = environment._getData(instrument, episodeStartDate-timedelta(days=environment.windowSize), episodeTimeSpan)
        environment.startDate = episodeStartDate

if __name__ == "__main__":
    ChangingTraining("microsoft", 1000, 365, date(2013, 1, 1), date(2021, 11, 1), 3.0)
    #SimpleTraining("microsoft", 100, 400, date(2018, 1, 1), 5)