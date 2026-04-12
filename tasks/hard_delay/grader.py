def grade(step_rewards):

    if not step_rewards:
        return 0.5

    avg = sum(step_rewards) / len(step_rewards)

    # reward longer sustained performance
    duration_bonus = min(len(step_rewards) / 15, 1.0)

    score = 0.5 * avg + 0.5 * duration_bonus

    return float(max(0.11, min(0.89, score)))
