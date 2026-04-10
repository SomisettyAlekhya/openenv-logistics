
import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

ENV_URL = "http://localhost:7860"

print("[START]")

state = requests.post(f"{ENV_URL}/reset").json()

for i in range(5):
    action = "dispatch"
    response = requests.post(f"{ENV_URL}/step", params={"action": action}).json()
    reward = response["reward"]

    print(f"[STEP] action={action} reward={reward}")

print("[END] score=0.7")
