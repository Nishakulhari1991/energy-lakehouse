"""Run the parser on the real API samples in tests/fixtures and show what it understood."""

import json

from energy_lakehouse.config import classify_series
from energy_lakehouse.parser import parse_response

for ds in ["price", "public_power"]:
    doc = json.load(open(f"tests/fixtures/{ds}_de_2026-11-19.json"))
    print(f"\n=== {ds} ===")
    print("license:", doc.get("license"))
    if ds == "public_power":
        for s in doc["series"]:
            print(f"   {s['name']:40} -> {classify_series(s['name'])}")
    recs = parse_response(doc, ds, "DE")
    print("rows:", len(recs), "| first:", recs[0].ts_utc, recs[0].value,
          "| missing values:", sum(r.value is None for r in recs))