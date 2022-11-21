from datetime import date

from Agent import TradingAgent
from TrainingEnviroment import StockSimulation


def SimpleTraining(instrument ,episodes, timeSpan, epidsodeStartDate):
    enviroment = StockSimulation(instrument, timeSpan, epidsodeStartDate)
    agent = TradingAgent(enviroment.inputSpace, enviroment.actionSpace, safeFile="./models/simple-microsoft-1.h5", epsilonDeqay=0.99)
    agent.load()

    for E in range(episodes):
        print("start episode: {:d}/{:d}, exploration: {:.2f}".format(E+1, episodes, agent.exploration))
        enviroment.reset()
        state = enviroment.getState()
        print(state)
        for t in range(enviroment.getEpisodeLength()):
            action = agent.predictAction(state)
            nextState, reward, finished = enviroment.action(action)
            agent.remember(state, action, reward, nextState, finished)
            state = nextState
            if finished:
                break
            agent.trainMemories(10)
            if t % 50 == 0:
                agent.save()
        print("total profit: {:.2f}".format(enviroment.profit))



if __name__ == "__main__":
    SimpleTraining("microsoft", 1000, 1000, date(2018, 1, 1))