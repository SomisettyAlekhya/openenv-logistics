
import random

class LogisticsEnv:

    def __init__(self):
        self.reset()

    def reset(self):
        self.pending_orders = 10
        self.vehicle_capacity = 5
        self.traffic_level = random.randint(0,2)
        return self.state()

    def state(self):
        return {
            "pending_orders": self.pending_orders,
            "vehicle_capacity": self.vehicle_capacity,
            "traffic_level": self.traffic_level
        }

    def step(self, action):

        reward = 0.0

        if action == "dispatch":
            delivered = min(self.vehicle_capacity, self.pending_orders)
            self.pending_orders -= delivered
            reward = delivered / 10

            if self.traffic_level == 2:
                reward *= 0.6

        elif action == "reroute":
            self.traffic_level = max(0, self.traffic_level - 1)
            reward = 0.3

        elif action == "delay":
            reward = 0.1

        reward = min(max(reward,0.0),1.0)

        done = self.pending_orders == 0

        return {
            "state": self.state(),
            "reward": reward,
            "done": done
        }
