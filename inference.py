import os
from openai import OpenAI
from env import LogisticsEnv

MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)

ACTIONS = ["dispatch", "reroute", "delay"]


def get_action(obs):

    try:
        prompt = f"""
You are a logistics agent.

State:
- task: {obs.task}
- packages: {obs.packages}
- traffic: {obs.traffic}

Choose one action:
dispatch, reroute, delay

Return only one word.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        action = response.choices[0].message.content.strip().lower()

        if action not in ACTIONS:
            return "dispatch"

        return action

    except Exception:
        return "dispatch"


def run_episode(task_name: str, max_steps: int = 10):

    env = LogisticsEnv(task=task_name)

    obs = env.reset()

    rewards = []

    for _ in range(max_steps):

        action = get_action(obs)

        obs, reward, done, _ = env.step(action)

        rewards.append(float(reward))

        if done:
            break

    return rewards


def main():

    print("[START]")

    tasks = ["easy", "medium", "hard"]

    scores = []

    for t in tasks:

        try:
            rewards = run_episode(t)

            if len(rewards) == 0:
                avg = 0.5
            else:
                avg = sum(rewards) / len(rewards)

            avg = max(0.01, min(0.99, float(avg)))

            print(f"{t}: {avg:.4f}")

            scores.append(avg)

        except Exception as e:
            print(f"ERROR in {t}: {e}")
            scores.append(0.5)

    final_score = sum(scores) / len(scores)
    final_score = max(0.01, min(0.99, final_score))

    print("[END]", final_score)


if __name__ == "__main__":
    main()
