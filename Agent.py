from collections import deque

class TradingAgent:
    def __init__(self, state_size, action_size) -> None:
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(2000)
        self.gamma = 0.9

        print("Hello, agent!")