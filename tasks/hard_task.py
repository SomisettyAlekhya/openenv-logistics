
def grade(env_state):
    score = 0.0

    if env_state["pending_orders"] == 0:
        score += 0.5

    if env_state["traffic_level"] == 0:
        score += 0.3

    if env_state["vehicle_capacity"] > 3:
        score += 0.2

    return min(score,1.0)
