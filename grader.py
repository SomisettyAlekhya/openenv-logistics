def grade(step_rewards):

    # ensure not empty
    if not step_rewards:
        return 0.6

    avg = sum(step_rewards) / len(step_rewards)

    # safe strict range
    score = 0.3 + 0.4 * avg

    return float(max(0.11, min(0.89, score)))
