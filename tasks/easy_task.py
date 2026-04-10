
def grade(env_state):
    if env_state["pending_orders"] == 0:
        return 1.0
    return max(0.0, 1 - env_state["pending_orders"]/10)
