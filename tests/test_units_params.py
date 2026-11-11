"""Units are parsed, converted and dimension-checked; parameter files load with valid bounds."""
import numpy as np
import pytest

from elisa_sim.params import load_raw, validate, sample_param, distribution_name
from elisa_sim.units import convert, parse_unit, UnitError


def test_basic_conversions():
    assert convert(1.0, "uL/min", "m^3/s") == pytest.approx(1e-9 / 60)
    assert convert(1.0, "M", "mol/m^3") == pytest.approx(1e3)
    assert convert(1.0, "1/(M*s)", "m^3/(mol*s)") == pytest.approx(1e-3)
    assert convert(1.0, "pg/mL", "g/m^3") == pytest.approx(1e-6)
    assert convert(1.0, "psi", "Pa") == pytest.approx(6894.757, rel=1e-6)
    assert convert(2.0, "percent RSD", "fraction") == pytest.approx(0.02)
    assert convert(5e5, "beads per 100 uL", "beads/m^3") == pytest.approx(5e12)
    assert convert(1.0, "A/min", "A/s") == pytest.approx(1 / 60)


def test_comment_groups_and_words_are_ignored():
    assert parse_unit("uL (at atmospheric pressure, each of two gaps)") == parse_unit("uL")
    assert parse_unit("M analyte-equivalent") == parse_unit("M")
    assert parse_unit("A/m^2 (at 100 uM AA)") == parse_unit("A/m^2")
    assert parse_unit("psi per (uL/min)") == parse_unit("psi*min/uL")


def test_dimension_mismatch_raises():
    with pytest.raises(UnitError):
        convert(1.0, "uL", "s")
    with pytest.raises(UnitError):
        convert(1.0, "HRP per conjugate", "m")
    with pytest.raises(UnitError):
        parse_unit("degC")


def test_every_yaml_unit_parses():
    params, _ = load_raw()
    problems = [p for p in validate(params) if "not parseable" in p]
    # degC (affine) is deliberately refused; it is not used by the model
    assert all("degC" in p for p in problems), problems


def test_bounds_ordered():
    params, _ = load_raw()
    assert [p for p in validate(params) if "outside" in p] == []


def test_sampling_respects_bounds_and_mode():
    params, _ = load_raw()
    rng = np.random.default_rng(1)
    for key in ("chem.antibodies.koff_capture", "chem.nsb.nsb_effective_rate_constant",
                "ma.fluid.viscosity", "hw.gamry.noise_rms_flow"):
        p = params[key]
        x = sample_param(p, 20000, rng)
        assert x.min() >= p.low and x.max() <= p.high
        if distribution_name(p) == "log-triangular":
            assert np.median(np.log(x)) == pytest.approx(np.log(x).mean(), abs=0.5)


def test_design_variables_not_sampled(ps):
    keys = ["hw.timing.accumulation_time", "chem.antibodies.conc_detection_antibody_typical",
            "chem.antibodies.kon_capture"]
    s = ps.sampleable(keys)
    assert s == ["chem.antibodies.kon_capture"]


def test_unit_change_does_not_change_value(ps):
    v1 = ps.get("hw.timing.sample_load_flow", "m^3/s")
    ps2 = ps.with_si({"hw.timing.sample_load_flow": (v1, "m^3/s")})
    assert ps2.get("hw.timing.sample_load_flow", "uL/min") == pytest.approx(ps.get("hw.timing.sample_load_flow",
                                                                                  "uL/min"))
