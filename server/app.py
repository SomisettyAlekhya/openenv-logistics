
from fastapi import FastAPI
from .environment import LogisticsEnv

app = FastAPI()
env = LogisticsEnv()

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: str):
    return env.step(action)

@app.get("/state")
def state():
    return env.state()
