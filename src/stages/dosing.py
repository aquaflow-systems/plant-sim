from dataclasses import dataclass

RAW_WATER_BASELINE_PH = 8.00
MAX_PH_SHIFT = 1.80
RESPONSE_RATE = 0.15


@dataclass
class DosingStage:
    ph_value: float = RAW_WATER_BASELINE_PH
    flow_rate: float = 0.0
    pump_speed: float = 45.0
    ph_setpoint: float = 7.00
    pump_state: bool = True

    def read(self) -> dict:
        return {
            "ph_value": round(self.ph_value, 2),
            "flow_rate": round(self.flow_rate, 1),
            "pump_speed": round(self.pump_speed, 1),
            "ph_setpoint": round(self.ph_setpoint, 2),
            "pump_state": self.pump_state,
        }

    def set_pump_speed(self, value: float) -> None:
        self.pump_speed = max(0.0, min(100.0, value))

    def set_ph_setpoint(self, value: float) -> None:
        self.ph_setpoint = value

    def set_pump_state(self, on: bool) -> None:
        self.pump_state = on

    def _target_ph(self) -> float:
        if not self.pump_state:
            return RAW_WATER_BASELINE_PH
        dose_fraction = self.pump_speed / 100.0
        return RAW_WATER_BASELINE_PH - MAX_PH_SHIFT * dose_fraction

    def step(self, dt: float, upstream_flow_lpm: float) -> None:
        self.flow_rate = upstream_flow_lpm

        target = self._target_ph()
        self.ph_value += (target - self.ph_value) * RESPONSE_RATE * dt
