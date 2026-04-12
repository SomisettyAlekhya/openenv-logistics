import random
from pydantic import BaseModel
from typing import Dict, Tuple


# -----------------------------
# Observation Model
# -----------------------------
class Observation(BaseModel):
    traffic: str
    packages: int
    task: str


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

        if isinstance(action, str):
            decision = action
        else:
            decision = action.decision

        reward = 0.4

        # -------------------------
        # ACTION LOGIC
        # -------------------------
        if decision == "dispatch":

            delivered = min(2, self.current_state.packages)
            self.current_state.packages -= delivered

            reward = 0.4 + 0.1 * delivered

            if self.current_state.traffic == "high":
                reward -= 0.15
            elif self.current_state.traffic == "low":
                reward += 0.15

        elif decision == "reroute":

            if self.current_state.traffic == "high":
                reward = 0.7
            elif self.current_state.traffic == "normal":
                reward = 0.6
            else:
                reward = 0.45

            self.current_state.traffic = "low"

        elif decision == "delay":

            reward = 0.3 + (0.02 * self.current_state.packages)

        else:
            reward = 0.3

        # -------------------------
        # RANDOMNESS (prevents collapse)
        # -------------------------
        reward += random.uniform(-0.05, 0.05)

        # -------------------------
        # SAFE CLAMP
        # -------------------------
        reward = max(0.1, min(0.9, reward))

        done = self.current_state.packages == 0

        return self.current_state, float(reward), done, {}

    def state(self) -> Dict:
        return self.current_state.dict()


# -----------------------------
# SAFE TASK FILTER (IMPORTANT FIX)
# -----------------------------
import os


def get_valid_tasks(tasks_dir="tasks"):
    """
    This ensures __pycache__ and invalid folders are NEVER treated as tasks
    """

    valid_tasks = []

    if not os.path.exists(tasks_dir):
        return valid_tasks

    for d in os.listdir(tasks_dir):

        path = os.path.join(tasks_dir, d)

        # must be folder
        if not os.path.isdir(path):
            continue

        # ❌ ignore system/cache folders
        if d.startswith("__"):
            continue

        # ❌ ignore non-task folders
        if "grader.py" not in os.listdir(path):
            continue

        if "task.yaml" not in os.listdir(path):
            continue

        valid_tasks.append(d)

    return valid_tasks
