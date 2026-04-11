from fastapi import FastAPI
import random

app = FastAPI()

state = {
    "step": 0,
    "done": False
}

ACTIONS = ["dispatch", "reroute", "delay"]


def reset_env():
    state["step"] = 0
    state["done"] = False
    return {"observation": "Start: Choose action"}


def step_env(action: str):

    if state["done"]:
        return {
            "observation": "done",
            "reward": 0,
            "done": True
        }

    if action not in ACTIONS:
        reward = -1
    else:
        reward = random.choice([0, 1, 2])

    state["step"] += 1
    obs = f"Step {state['step']} received action={action}"

    if state["step"] >= 5:
        state["done"] = True

    return {
        "observation": obs,
        "reward": reward,
        "done": state["done"]
    }


# ---------------------------
# REQUIRED FOR VALIDATOR
# ---------------------------

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
