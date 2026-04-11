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

        if self.task == "easy":
            packages = 5
            traffic = "low"
        elif self.task == "medium":
            packages = 10
            traffic = "normal"
        else:
            packages = 15
            traffic = "high"

        self.current_state = Observation(
            traffic=traffic,
            packages=packages,
            task=self.task
        )

        return self.current_state


    def step(self, action) -> Tuple[Observation, float, bool, Dict]:

        # ✅ SUPPORT BOTH STRING + Action OBJECT
        if isinstance(action, str):
            decision = action
        else:
            decision = action.decision

        reward = 0.5  # safe default

        # -------------------------
        # Action logic
        # -------------------------

        if decision == "dispatch":
            reward = 0.6

            if self.current_state.traffic == "high":
                reward *= 0.7
            elif self.current_state.traffic == "low":
                reward += 0.2

            # slower decay → more steps (IMPORTANT)
            self.current_state.packages = max(0, self.current_state.packages - 1)

        elif decision == "reroute":
            reward = 0.7 if self.current_state.traffic != "low" else 0.4
            self.current_state.traffic = "low"

        elif decision == "delay":
            reward = 0.5

        else:
            reward = 0.3  # NEVER 0

        # -------------------------
        # SAFE REWARD RANGE (CRITICAL)
        # -------------------------

        reward = 0.2 + 0.6 * reward   # center scaling
        reward = max(0.1, min(0.9, reward))

        # -------------------------
        # DONE CONDITION
        # -------------------------

        done = self.current_state.packages == 0

        return self.current_state, float(reward), done, {}

    def state(self) -> Dict:
        return self.current_state.dict()
