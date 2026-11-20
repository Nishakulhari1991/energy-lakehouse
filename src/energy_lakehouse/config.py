"""Static configuration: markets, API datasets and how series names map to fuel types."""

from __future__ import annotations

import re
from dataclasses import dataclass

API_URL = "https://api.energy-charts.info/v2"


@dataclass(frozen=True)
class Market:
    """A market = a country (for production data) + its day-ahead bidding zone (for prices)."""

    code: str
    country: str
    bidding_zone: str
    timezone: str


MARKETS: dict[str, Market] = {
    m.code: m
    for m in [
        Market("DE", "de", "DE-LU", "Europe/Berlin"),
        Market("FR", "fr", "FR", "Europe/Paris"),
        Market("NL", "nl", "NL", "Europe/Amsterdam"),
        Market("AT", "at", "AT", "Europe/Vienna"),
        Market("BE", "be", "BE", "Europe/Brussels"),
        Market("PL", "pl", "PL", "Europe/Warsaw"),
        Market("DK1", "dk", "DK1", "Europe/Copenhagen"),
        Market("ES", "es", "ES", "Europe/Madrid"),
    ]
}

DEFAULT_MARKETS = ["DE", "FR", "NL", "AT"]

# dataset -> (API endpoint, query parameter, Market attribute that fills it)
DATASETS: dict[str, tuple[str, str, str]] = {
    "price": ("price", "bzn", "bidding_zone"),
    "public_power": ("public_power", "country", "country"),
}

RENEWABLE_FUELS = {
    "biomass", "geothermal", "hydro_run_of_river", "hydro_reservoir", "hydro_other",
    "solar", "wind_onshore", "wind_offshore", "other_renewable",
}
VARIABLE_RENEWABLE_FUELS = {"solar", "wind_onshore", "wind_offshore"}

# Order matters: first match wins. Value None = not a generation series (skip it).
_FUEL_RULES: list[tuple[str, str | None]] = [
    (r"residual load", None),
    (r"share", None),                      # "Renewable share of load" etc. are ratios, not MW
    (r"cross.?border", None),              # imports/exports
    (r"consumption", None),                # e.g. pumped storage pumping
    (r"^load$|^load \(", "LOAD"),          # total load: kept, but as its own dataset
    (r"battery", None),                    # storage discharge, would double count
    (r"solar", "solar"),
    (r"wind.*off", "wind_offshore"),
    (r"wind.*on", "wind_onshore"),
    (r"^wind$", "wind_onshore"),
    (r"biomass", "biomass"),
    (r"geothermal", "geothermal"),
    (r"run.?of.?river", "hydro_run_of_river"),
    (r"reservoir", "hydro_reservoir"),
    (r"pumped storage", "hydro_pumped_storage"),
    (r"hydro", "hydro_other"),
    (r"nuclear", "nuclear"),
    (r"lignite|brown coal", "lignite"),
    (r"coal.?derived gas", "coal_derived_gas"),
    (r"hard coal|^coal$|fossil coal", "hard_coal"),
    (r"gas", "gas"),
    (r"oil", "oil"),
    (r"waste", "waste"),
    (r"other renewable", "other_renewable"),
    (r"other", "other"),
]


def classify_series(name: str) -> str | None:
    """Map a public_power series name to a fuel id, 'LOAD', or None (not generation).

    Unknown names map to 'unknown' so they show up in data-quality checks instead of
    silently vanishing.
    """
    n = name.strip().lower()
    for pattern, fuel in _FUEL_RULES:
        if re.search(pattern, n):
            return fuel
    return "unknown"


def is_open_licence(licence: str | None) -> bool:
    """True if the data may be published (CC BY 4.0). Everything else stays private."""
    return bool(licence) and "cc by" in licence.lower()