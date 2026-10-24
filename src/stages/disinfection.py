from dataclasses import dataclass

BASELINE_PATHOGEN_INDEX = 850.0
NOMINAL_CHLORINE_DOSE = 1.20
RESPONSE_RATE = 0.25


@dataclass
class DisinfectionStage:
    chlorine_dose: float = NOMINAL_CHLORINE_DOSE
    pathogen_index: float = BASELINE_PATHOGEN_INDEX

    def read(self) -> dict:
        return {
            "chlorine_dose": round(self.chlorine_dose, 2),
            "pathogen_index": round(self.pathogen_index, 0),
        }

    def set_chlorine_dose(self, value: float) -> None:
        self.chlorine_dose = max(0.0, value)

    def _effectiveness(self, upstream_ph: float) -> float:
        """0-1 multiplier on how well the chlorine dose actually works."""
        distance_from_neutral = abs(7.0 - upstream_ph)
        penalty = min(0.9, distance_from_neutral * 0.35)
        return max(0.1, 1.0 - penalty)

    def step(self, dt: float, upstream_ph: float) -> None:
        effectiveness = self._effectiveness(upstream_ph)
        kill_rate = self.chlorine_dose * effectiveness

        target = max(20.0, BASELINE_PATHOGEN_INDEX - kill_rate * 500)
        self.pathogen_index += (target - self.pathogen_index) * RESPONSE_RATE * dt