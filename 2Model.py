from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass(frozen=True)
class IDMParams:
    v0: float = 30.0
    a: float = 1.0
    b: float = 1.5
    s0: float = 2.0
    T: float = 1.5
    delta: int = 4

def idm_accel(ego: Dict[str, Any], lead: Dict[str, Any] | None, params: IDMParams) -> float:
    v = ego.get("v", 0.0)
    if lead is None:
        target_v = ego.get("target_v")
        if target_v is not None:
            k = 1.0 / max(params.T, 1e-6)
            a_cmd = k * (target_v - v)
            return max(-params.b, min(params.a, a_cmd))
        return params.a * (1 - (v / params.v0) ** params.delta)
    L = lead.get("length", 4.5)
    s = max(1e-3, lead["x"] - ego.get("x", 0.0) - L)
    dv = v - lead.get("v", 0.0)
    s_star = params.s0 + max(0.0, v * params.T + v * dv / (2 * (params.a * params.b) ** 0.5))
    return params.a * (1 - (v / params.v0) ** params.delta - (s_star / s) ** 2)

def step(state: Dict[str, Any], params: IDMParams) -> Dict[str, Any]:
    vehicles: List[Dict[str, Any]] = state["vehicles"]
    dt = state["dt"]
    n = len(vehicles)
    acc = [0.0] * n
    for i in range(n):
        lead = vehicles[i + 1] if i + 1 < n else None
        acc[i] = idm_accel(vehicles[i], lead, params)
    for i in range(n):
        ego = vehicles[i]
        ego["a"] = acc[i]
        v_new = max(0.0, ego.get("v", 0.0) + acc[i] * dt)
        x_new = ego.get("x", 0.0) + v_new * dt
        ego["v"] = v_new
        ego["x"] = x_new
    state["t"] = state["t"] + dt
    return state
