import random
from dataclasses import dataclass

BASELINE_TURBIDITY_NTU = 4.5
EFFICIENCY_DRIFT_PER_HOUR = 0.02
MIN_EFFICIENCY = 80.0


@dataclass
class FiltrationStage:
    turbidity_in: float = BASELINE_TURBIDITY_NTU
    turbidity_out: float = 0.0
    filter_efficiency: float = 97.0

    def read(self) -> dict:
        return {
            "turbidity_in": round(self.turbidity_in, 1),
            "turbidity_out": round(self.turbidity_out, 1),
            "filter_efficiency": round(self.filter_efficiency, 1),
        }

    def step(self, dt: float, upstream_ph: float) -> None:
        self.turbidity_in = BASELINE_TURBIDITY_NTU + random.uniform(-0.3, 0.3)

        if upstream_ph < 6.5 or upstream_ph > 8.5:
            self.turbidity_in += abs(7.0 - upstream_ph) * 1.5

        self.filter_efficiency = max(
            MIN_EFFICIENCY,
            self.filter_efficiency - EFFICIENCY_DRIFT_PER_HOUR * (dt / 3600.0),
        )

        self.turbidity_out = self.turbidity_in * (1 - self.filter_efficiency / 100.0)