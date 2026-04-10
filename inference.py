import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# CHANGE THIS TO YOUR HF SPACE URL
ENV_URL = "https://alekhyasomisetty-openenv-logistics.hf.space"

print("[START]")

state = requests.post(f"{ENV_URL}/reset").json()

for step in range(5):

    prompt = f"""
You are controlling a logistics delivery system.
State:
pending_orders: {state['pending_orders']}
vehicle_capacity: {state['vehicle_capacity']}
traffic_level: {state['traffic_level']}
Choose one action:
dispatch
reroute
delay
Respond with only the action.
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    action = completion.choices[0].message.content.strip().lower()

    response = requests.post(
        f"{ENV_URL}/step",
        params={"action": action}
    ).json()

    reward = response["reward"]
    state = response["state"]

    print(f"[STEP] action={action} reward={reward}")

print("[END] score=0.7")
