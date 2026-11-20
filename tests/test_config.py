import pytest

from energy_lakehouse.config import DEFAULT_MARKETS, MARKETS, classify_series, is_open_licence


@pytest.mark.parametrize("name,fuel", [
    ("Solar", "solar"), ("Wind onshore", "wind_onshore"), ("Wind offshore", "wind_offshore"),
    ("Fossil brown coal / lignite", "lignite"), ("Fossil hard coal", "hard_coal"),
    ("Fossil coal-derived gas", "coal_derived_gas"), ("Fossil gas", "gas"),
    ("Hydro Run-of-River", "hydro_run_of_river"), ("Hydro water reservoir", "hydro_reservoir"),
    ("Hydro pumped storage", "hydro_pumped_storage"), ("Nuclear", "nuclear"), ("Others", "other"),
    ("Load", "LOAD"),
    ("Residual load", None), ("Renewable share of load", None),
    ("Hydro pumped storage consumption", None), ("Cross border electricity trading", None),
    ("Something brand new", "unknown"),
])
def test_classify_series(name, fuel):
    assert classify_series(name) == fuel


def test_open_licence_detection():
    assert is_open_licence("CC BY 4.0 (creativecommons.org/licenses/by/4.0) from Bundesnetzagentur")
    assert not is_open_licence("Restricted to private and internal use")
    assert not is_open_licence(None)


def test_default_markets_are_configured():
    assert all(m in MARKETS for m in DEFAULT_MARKETS)
    assert MARKETS["DE"].bidding_zone == "DE-LU"