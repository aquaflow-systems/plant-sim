from dataclasses import dataclass


@dataclass
class DistributionStage:
    final_ph: float = 7.0
    final_turbidity: float = 0.0
    final_pathogen_index: float = 0.0
    distribution_flow: float = 0.0

    def read(self) -> dict:
        return {
            "final_ph": round(self.final_ph, 2),
            "final_turbidity": round(self.final_turbidity, 1),
            "final_pathogen_index": round(self.final_pathogen_index, 0),
            "distribution_flow": round(self.distribution_flow, 1),
        }

    def step(
        self,
        dt: float,
        upstream_ph: float,
        upstream_turbidity: float,
        upstream_pathogen_index: float,
        upstream_flow: float,
    ) -> None:
        self.final_ph = upstream_ph
        self.final_turbidity = upstream_turbidity
        self.final_pathogen_index = upstream_pathogen_index
        self.distribution_flow = upstream_flow
