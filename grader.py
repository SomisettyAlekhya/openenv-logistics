def grade(step_rewards):

    if not step_rewards:
        return 0.51  # NEVER 0

    score = sum(step_rewards) / len(step_rewards)

    # STRICT (0,1)
    score = 0.1 + 0.8 * score

    return max(0.01, min(0.99, float(score)))
