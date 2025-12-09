import importlib.util
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ScenarioSetup = load_module("/Users/panyu/Documents/trae_projects/simulation/1ScenarioSetup.py", "ScenarioSetup")
Model = load_module("/Users/panyu/Documents/trae_projects/simulation/2Model.py", "Model")

cfg = ScenarioSetup.ScenarioConfig(seed=42, init_vehicles=25, dt=0.5, road_length=3000.0, vehicle_length=4.5, net_spacing=10.0, leader_speed=0.0)
scn = ScenarioSetup.Scenario(cfg)
state = scn.build_state()
params = Model.IDMParams(v0=30.0, a=1.0, b=1.5, s0=2.0, T=1.5)

T = 300.0
steps = int(np.ceil(T / state["dt"]))
n = len(state["vehicles"])
speeds = np.zeros((steps, n))
times = np.zeros(steps)

for k in range(steps):
    times[k] = state["t"]
    speeds[k, :] = [v["v"] for v in state["vehicles"]]
    Model.step(state, params)

plt.figure(figsize=(8, 6))
im = plt.imshow(
    speeds,
    aspect="auto",
    origin="lower",
    extent=[1, n, times[0], times[-1]],
    cmap="turbo",
    norm=Normalize(vmin=0.0, vmax=max(params.v0, speeds.max()))
)
plt.colorbar(im, label="speed (m/s)")
plt.xlabel("car number")
plt.ylabel("time (s)")
plt.title("Speed vs Time (IDM)")
plt.show()