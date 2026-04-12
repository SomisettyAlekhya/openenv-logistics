def grade(step_rewards):
    if not step_rewards:
        return 0.6

    avg = sum(step_rewards) / len(step_rewards)

    # keep strictly between (0,1)
    score = 0.3 + 0.4 * avg

    if score <= 0.0:
        score = 0.11
    if score >= 1.0:
        score = 0.89

    return float(score)
