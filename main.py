from Agent import TradingAgent
from TrainingEnviroment import StockSimulation


def SimpleTraning(instrument ,episodes, episodeLength, epidsodeStartDate):
    enviroment = StockSimulation(instrument, episodeLength, epidsodeStartDate)
    agent = TradingAgent(enviroment.inputSpace, enviroment.actionSpace)

    for E in range(episodes):
        print("start episode: {:d}/{:d}, exploration: {:.2}".format(E, episodes, agent.exploration))
        enviroment.reset()
        state = enviroment.getState()
        for t in range(episodeLength):
            action = agent.predictAction(state)
            nextState, reward, finished = enviroment.action(action)
            agent.remember(state, action, reward, nextState, finished)
            state = nextState
            if finished:
                break
            agent.trainMemories(10)



if __name__ == "__main__":
    SimpleTraning("microsoft", 10, 10, 1)