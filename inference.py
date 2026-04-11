import os
import requests
from openai import OpenAI

from env import LogisticsEnv


# -----------------------------
# LLM SETUP
# -----------------------------
MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)


# -----------------------------
# AGENT POLICY
# -----------------------------
ACTIONS = ["dispatch", "reroute", "delay"]


def get_action(obs):

    prompt = f"""
You are a logistics agent.

State:
- task: {obs['task']}
- packages: {obs['packages']}
- traffic: {obs['traffic']}

Choose ONE action from:
dispatch, reroute, delay

Return only one word.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        action = response.choices[0].message.content.strip().lower()

        if action not in ACTIONS:
            action = "dispatch"

        return action

    except Exception:
        return "dispatch"


# -----------------------------
# RUN EPISODE
# -----------------------------
def run_episode(task_name: str, max_steps: int = 10):

    env = LogisticsEnv(task=task_name)

    obs = env.reset()

    step_rewards = []

    for _ in range(max_steps):

        action = get_action(obs)

        obs, reward, done, _ = env.step(action)

        step_rewards.append(reward)

        if done:
            break

    return step_rewards


# -----------------------------
# MAIN EVALUATION
# -----------------------------
def main():

    print("[START] inference running")

    tasks = ["easy", "medium", "hard"]

    all_scores = {}

    for t in tasks:

        rewards = run_episode(t)

        avg_reward = sum(rewards) / len(rewards) if rewards else 0.0

        all_scores[t] = avg_reward

        print(f"[TASK] {t} | avg_reward = {avg_reward:.4f}")

    final_score = sum(all_scores.values()) / len(all_scores)

    print(f"[END] final_score = {final_score:.4f}")


if __name__ == "__main__":
    main()
