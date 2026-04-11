def grade(step_rewards):

    if not step_rewards:
        return 0.51  # NEVER 0

    score = sum(step_rewards) / len(step_rewards)

    # FORCE INTO STRICT (0,1)
    score = 0.2 + 0.6 * score

    # safety clamp (NEVER boundaries)
    if score <= 0.0:
        score = 0.11
    if score >= 1.0:
        score = 0.89

    return float(score)
