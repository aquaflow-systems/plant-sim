from dataclasses import dataclass

TANK_CAPACITY_PCT = 100.0
NOMINAL_DEMAND_LPM = 120.0
MAX_INTAKE_LPM = 150.0


@dataclass
class RawWaterStage:
    tank_level: float = 60.0
    intake_pump_speed: float = 70.0

    def read(self) -> dict:
        return {
            "tank_level": round(self.tank_level, 1),
            "intake_pump_speed": round(self.intake_pump_speed, 1),
        }

    def set_intake_pump_speed(self, value: float) -> None:
        self.intake_pump_speed = max(0.0, min(100.0, value))

    def outflow_lpm(self) -> float:
        """Flow handed to the dosing stage. Capped by what the tank can supply."""
        if self.tank_level <= 0:
            return 0.0
        return NOMINAL_DEMAND_LPM

    def step(self, dt: float) -> None:
        inflow_lpm = MAX_INTAKE_LPM * (self.intake_pump_speed / 100.0)
        outflow_lpm = self.outflow_lpm()

        net_lpm = inflow_lpm - outflow_lpm
        self.tank_level += net_lpm * 0.05 * (dt / 60.0)
        self.tank_level = max(0.0, min(TANK_CAPACITY_PCT, self.tank_level))
