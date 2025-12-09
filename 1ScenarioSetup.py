from dataclasses import dataclass
import random

@dataclass(frozen=True)
class ScenarioConfig:
    seed: int = 42
    init_vehicles: int = 20
    dt: float = 0.1
    road_length: float = 5000.0
    vehicle_length: float = 3.5
    net_spacing: float = 10.0
    leader_speed: float = 0.0

class Scenario:
    def __init__(self, config: ScenarioConfig):
        self.config = config
        self.rng = random.Random(config.seed)
        self.next_id = 1
        self.next_arrival = 0.0
    def build_state(self):
        vehicles = []
        L = self.config.vehicle_length
        s_net = self.config.net_spacing
        spacing_total = L + s_net
        for i in range(self.config.init_vehicles):
            x = i * spacing_total
            vehicles.append({"id": self.next_id, "x": x, "v": 0.0, "a": 0.0, "length": L})
            self.next_id += 1
        if vehicles:
            vehicles[0]["target_v"] = self.config.leader_speed
        return {"t": 0.0, "dt": self.config.dt, "vehicles": vehicles, "road_length": self.config.road_length}
    # def inject_vehicles(self, t: float, state: dict):
    #     while t >= self.next_arrival:
    #         state["vehicles"].append({"id": self.next_id, "x": 0.0, "v": 0.0, "a": 0.0})
    #         self.next_id += 1
    #         self.next_arrival += self.config.arrival_interval