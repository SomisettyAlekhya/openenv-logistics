def grade(step_rewards):

    if not step_rewards:
        return 0.5

    # reward higher average delivery efficiency
    avg = sum(step_rewards) / len(step_rewards)

    # encourage shorter episodes (faster completion)
    length_penalty = min(len(step_rewards) / 10, 1.0)

    score = 0.5 * avg + 0.5 * (1 - length_penalty)

    return float(max(0.11, min(0.89, score)))
