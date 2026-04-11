import os
import requests
from openai import OpenAI

print("[START]")

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")
ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

# reset environment
try:
    reset_resp = requests.post(f"{ENV_URL}/reset", timeout=5).json()
except Exception as e:
    print("Reset error:", e)
    reset_resp = {}

obs = reset_resp.get("observation", "")

total_reward = 0
done = False

for i in range(5):

    # ask LLM based on observation
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Observation: {obs}

Choose ONE action from: dispatch, reroute, delay
Return ONLY the word.
"""
                }
            ]
        )

        action = response.choices[0].message.content.strip().lower()
        action = action.split()[0]  # safety cleanup

    except Exception as e:
        print("LLM error:", e)
        action = "dispatch"

    # environment step
    try:
        step_resp = requests.post(
            f"{ENV_URL}/step",
            params={"action": action},
            timeout=5
        ).json()

        obs = step_resp.get("observation", obs)
        reward = step_resp.get("reward", 0)
        done = step_resp.get("done", False)

    except Exception as e:
        print("Step error:", e)
        reward = 0
        done = True

    total_reward += reward

    print(f"[STEP {i}] action={action} reward={reward}")

    if done:
        break

print(f"[END] score={total_reward}")
