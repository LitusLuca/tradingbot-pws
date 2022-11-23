from datetime import date

from Agent import TradingAgent
from TrainingEnvironment import StockSimulation


def SimpleTraining(instrument ,episodes, timeSpan, episodeStartDate, iteration):
    environment = StockSimulation(instrument, timeSpan, episodeStartDate, results="./results/simple-{}-{}.xlsx".format(instrument, iteration))
    agent = TradingAgent(environment.inputSpace, environment.actionSpace, safeFile="./models/simple-{}-{}.h5".format(instrument, iteration), epsilonDeqay=0.99)
    agent.load()

    for E in range(episodes):
        print("start episode: {:d}/{:d}, exploration: {:.2f}".format(E+1, episodes, agent.exploration))
        
        state = environment.getState()
        print(state)
        for t in range(environment.getEpisodeLength()):
            action = agent.predictAction(state)
            nextState, reward, finished = environment.action(action)
            agent.remember(state, action, reward, nextState, finished)
            state = nextState
            if finished:
                break
            agent.trainMemories(10)
            if t % 50 == 0:
                agent.save()
        print("total profit: {:.2f}".format(environment.profit))
        environment.reset()



if __name__ == "__main__":
    SimpleTraining("microsoft", 100, 200, date(2018, 1, 1), 2)