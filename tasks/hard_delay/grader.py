def grade(step_rewards):
    if not step_rewards:
        return 0.51  # never 0

    score = sum(step_rewards) / len(step_rewards)

    # force strict range (0,1)
    score = 0.1 + 0.8 * score

    # safety clamp (never hit boundaries)
    if score <= 0.0:
        score = 0.11
    if score >= 1.0:
        score = 0.89

    return float(score)
