from dataclasses import dataclass, field

from .stages import (
    DisinfectionStage,
    DistributionStage,
    DosingStage,
    FiltrationStage,
    RawWaterStage,
)


@dataclass
class Plant:
    raw_water: RawWaterStage = field(default_factory=RawWaterStage)
    dosing: DosingStage = field(default_factory=DosingStage)
    filtration: FiltrationStage = field(default_factory=FiltrationStage)
    disinfection: DisinfectionStage = field(default_factory=DisinfectionStage)
    distribution: DistributionStage = field(default_factory=DistributionStage)

    def step(self, dt: float) -> None:
        self.raw_water.step(dt)

        self.dosing.step(dt, upstream_flow_lpm=self.raw_water.outflow_lpm())

        self.filtration.step(dt, upstream_ph=self.dosing.ph_value)

        self.disinfection.step(dt, upstream_ph=self.dosing.ph_value)

        self.distribution.step(
            dt,
            upstream_ph=self.dosing.ph_value,
            upstream_turbidity=self.filtration.turbidity_out,
            upstream_pathogen_index=self.disinfection.pathogen_index,
            upstream_flow=self.dosing.flow_rate,
        )

    def read_all(self) -> dict:
        return {
            "raw_water": self.raw_water.read(),
            "dosing": self.dosing.read(),
            "filtration": self.filtration.read(),
            "disinfection": self.disinfection.read(),
            "distribution": self.distribution.read(),
        }
