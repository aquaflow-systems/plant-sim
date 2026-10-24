import pytest

from src.stages.dosing import RAW_WATER_BASELINE_PH, DosingStage


def test_ph_drifts_back_to_baseline_when_pump_is_off():
    stage = DosingStage(ph_value=7.0, pump_state=False)

    for _ in range(200):
        stage.step(dt=1.0, upstream_flow_lpm=100.0)

    assert stage.ph_value == pytest.approx(RAW_WATER_BASELINE_PH, abs=0.05)


def test_higher_pump_speed_lowers_ph_more():
    low_dose = DosingStage(ph_value=RAW_WATER_BASELINE_PH, pump_state=True, pump_speed=20)
    high_dose = DosingStage(ph_value=RAW_WATER_BASELINE_PH, pump_state=True, pump_speed=90)

    for _ in range(50):
        low_dose.step(dt=1.0, upstream_flow_lpm=100.0)
        high_dose.step(dt=1.0, upstream_flow_lpm=100.0)

    assert high_dose.ph_value < low_dose.ph_value


def test_flow_rate_mirrors_upstream():
    stage = DosingStage()
    stage.step(dt=1.0, upstream_flow_lpm=87.0)
    assert stage.flow_rate == 87.0


def test_pump_speed_is_clamped_to_valid_range():
    stage = DosingStage()

    stage.set_pump_speed(150)
    assert stage.pump_speed == 100.0

    stage.set_pump_speed(-10)
    assert stage.pump_speed == 0.0
