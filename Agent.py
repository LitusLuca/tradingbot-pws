from collections import deque

class TradingAgent:
    def __init__(self, state_size, action_size) -> None:
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(2000)
        self.gamma = 0.9
        self.exploration = 1.0
        self.exploration_decay = 0.99
        self.exploration_min = 0.05
        self.model = self._createModel()

        print("Hello, agent!")
    def predict_action(self, state):
        pass
