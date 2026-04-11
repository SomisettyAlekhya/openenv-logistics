def grade(step_rewards):
    if not step_rewards:
        return 0.0

    score = sum(step_rewards) / len(step_rewards)

    # IMPORTANT: strict clamp
    return max(0.0, min(1.0, float(score)))
