import random

class LogisticsEnv:

    def __init__(self):
        self.reset()

    def reset(self):
        self.pending_orders = 10
        self.vehicle_capacity = 5
        self.traffic_level = random.randint(0,2)
        self.total_delivered = 0

        return self.state()

    def state(self):
        return {
            "pending_orders": self.pending_orders,
            "vehicle_capacity": self.vehicle_capacity,
            "traffic_level": self.traffic_level,
            "total_delivered": self.total_delivered
        }

    def step(self, action):

        reward = 0.0

        # Dispatch action
        if action == "dispatch":

            delivered = min(self.vehicle_capacity, self.pending_orders)
            self.pending_orders -= delivered
            self.total_delivered += delivered

            # delivery efficiency reward
            reward += delivered / 10

            # traffic penalty
            if self.traffic_level == 2:
                reward *= 0.6

        # Reroute action
        elif action == "reroute":

            if self.traffic_level > 0:
                self.traffic_level -= 1
                reward += 0.3
            else:
                reward += 0.1

        # Delay action
        elif action == "delay":

            reward += 0.05

        # completion bonus
        if self.pending_orders == 0:
            reward += 0.3

        reward = max(0.0, min(1.0, reward))

        done = self.pending_orders == 0

        return {
            "state": self.state(),
            "reward": reward,
            "done": done
        }
