from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# simple in-memory state
state = {
    "step": 0,
    "done": False
}

ACTIONS = ["dispatch", "reroute", "delay"]


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/reset")
def reset():
    state["step"] = 0
    state["done"] = False

    observation = "Start: Choose action"
    return {
        "observation": observation
    }


@app.post("/step")
def step(action: str):

    if state["done"]:
        return {
            "observation": "done",
            "reward": 0,
            "done": True
        }

    # validate action
    if action not in ACTIONS:
        reward = -1
    else:
        reward = random.choice([0, 1, 2])  # dummy reward logic

    state["step"] += 1

    observation = f"Step {state['step']} received action={action}"

    if state["step"] >= 5:
        state["done"] = True

    return {
        "observation": observation,
        "reward": reward,
        "done": state["done"]
    }
