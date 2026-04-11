def grade(step_rewards):

    if not step_rewards:
        return 0.5  # IMPORTANT: avoid 0.0

    score = sum(step_rewards) / len(step_rewards)

    # scale into (0,1) strictly
    score = score * 0.9 + 0.05

    # ensure strict bounds (never 0 or 1)
    if score <= 0.0:
        score = 0.01
    if score >= 1.0:
        score = 0.99

    return float(score)
