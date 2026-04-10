def grade(state):

    score = 0.0

    if state["pending_orders"] == 0:
        score += 0.5

    if state["traffic_level"] == 0:
        score += 0.3

    if state["total_delivered"] >= 10:
        score += 0.2

    return min(score,1.0)
