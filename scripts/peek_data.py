"""Show the real API data as simple tables, so we can see what we are working with."""

import json

# ---------- 1. Day-ahead PRICES ----------
price = json.load(open("tests/fixtures/price_de_2026-11-19.json"))
print("=" * 70)
print("PRICES  | market:", price["bidding_zone"], "| unit:", price["unit"],
      "| every", price["interval_minutes"], "min")
print("licence:", price.get("license"))
print("-" * 70)
print(f"{'time (German local)':28} price")
for point in price["data"][:8]:
    print(f"{point['timestamp']:28} {point['values']['day_ahead_price']}")
print(f"... {len(price['data'])} rows in total for the day")

# ---------- 2. POWER per fuel type ----------
power = json.load(open("tests/fixtures/public_power_de_2026-11-19.json"))
print()
print("=" * 70)
print("POWER   | country:", power["country"], "| unit:", power["unit"],
      "| every", power["interval_minutes"], "min")
print("licence:", power.get("license"))
print("-" * 70)
first, noon = power["data"][0], power["data"][48]
print(f"{'series (what is measured)':40} {'00:00':>10} {'12:00':>10}")
for s in power["series"]:
    sid = s["id"]
    print(f"{s['name']:40} {str(first['values'].get(sid)):>10} {str(noon['values'].get(sid)):>10}")
print(f"... {len(power['data'])} timestamps x {len(power['series'])} series")