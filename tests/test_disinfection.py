from src.stages.disinfection import DisinfectionStage


def test_pathogen_index_drops_with_dosing_at_neutral_ph():
    stage = DisinfectionStage(chlorine_dose=1.2, pathogen_index=850.0)

    for _ in range(50):
        stage.step(dt=1.0, upstream_ph=7.0)

    assert stage.pathogen_index < 850.0


def test_effectiveness_is_worse_far_from_neutral_ph():
    neutral = DisinfectionStage(chlorine_dose=1.2, pathogen_index=850.0)
    off_ph = DisinfectionStage(chlorine_dose=1.2, pathogen_index=850.0)

    for _ in range(50):
        neutral.step(dt=1.0, upstream_ph=7.0)
        off_ph.step(dt=1.0, upstream_ph=9.5)

    assert off_ph.pathogen_index > neutral.pathogen_index


def test_chlorine_dose_is_clamped_to_non_negative():
    stage = DisinfectionStage()
    stage.set_chlorine_dose(-5)
    assert stage.chlorine_dose == 0.0
