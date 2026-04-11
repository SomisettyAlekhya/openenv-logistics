import random
from pydantic import BaseModel
from typing import Dict, Tuple


# -----------------------------
# Structured IO (Pydantic)
# -----------------------------

class Observation(BaseModel):
    traffic: str
    packages: int
    task: str


class Action(BaseModel):
    decision: str


class Reward(BaseModel):
    value: float


# -----------------------------
# Logistics Environment
# -----------------------------

class LogisticsEnv:

    def __init__(self, task: str = "easy"):
        assert task in ["easy", "medium", "hard"]
        self.task = task
        self.reset()

    def reset(self) -> Observation:

        # task-based difficulty scaling
        if self.task == "easy":
            packages = 5
            traffic_level = "low"
        elif self.task == "medium":
            packages = 10
            traffic_level = "normal"
        else:
            packages = 15
            traffic_level = "high"

        self.current_state = Observation(
            traffic=traffic_level,
            packages=packages,
            task=self.task
        )

        return self.current_state

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict]:

        reward = 0.0

        # -------------------------
        # Action logic
        # -------------------------

        if action.decision == "dispatch":
            reward = 0.6

            # bonus/penalty based on traffic
            if self.current_state.traffic == "high":
                reward *= 0.7
            elif self.current_state.traffic == "low":
                reward += 0.2

            # reduce packages
            self.current_state.packages = max(0, self.current_state.packages - 2)

        elif action.decision == "reroute":
            reward = 0.8 if self.current_state.traffic != "low" else 0.3

            # improve traffic slightly
            self.current_state.traffic = "low"

        elif action.decision == "delay":
            reward = 0.4

        else:
            reward = 0.0  # invalid action

        # -------------------------
        # Episode termination
        # -------------------------

        done = self.current_state.packages == 0

        # STRICT clamp (IMPORTANT for Phase-2)
        reward = max(0.01, min(0.99, reward))

        return self.current_state, reward, done, {}

    def state(self) -> Dict:
        return self.current_state.dict()
