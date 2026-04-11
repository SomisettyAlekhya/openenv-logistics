from pydantic import BaseModel
from typing import Dict

class Observation(BaseModel):
    traffic: str
    packages: int

class Action(BaseModel):
    decision: str

class Reward(BaseModel):
    value: float


class LogisticsEnv:

    def reset(self) -> Observation:
        self.current_state = Observation(
            traffic="normal",
            packages=5
        )
        return self.current_state

    def step(self, action: Action):
        reward = 0.0

        if action.decision == "dispatch":
            reward = 0.6
        elif action.decision == "reroute":
            reward = 0.8
        elif action.decision == "delay":
            reward = 0.4

        done = True

        return self.current_state, reward, done, {}

    def state(self) -> Dict:
        return self.current_state.dict()
