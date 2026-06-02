"""
restaurant_impact.py
====================
Hypothetical order volume impact model for 3 restaurant types:
  QSR (Quick Service Restaurant) — e.g. Mad Over Donuts, 99 Pancakes
  Dine-in (Full Service Restaurant) — e.g. casual/fine dining
  PBCL (Pub, Bar, Café, Lounge) — e.g. Barista, craft beer pubs

Each restaurant type responds differently to the same event/weather.
Model returns:
  - base_orders: typical daily orders (normalised baseline = 100)
  - predicted_orders: after event/weather multipliers
  - pct_change: % lift or drop
  - confidence: Low / Medium / High
  - factors: list of what drove the change
"""

from datetime import date, timedelta
from data.events_db import EVENTS_DB, _event_applies_to_geo

# ── Baseline orders (normalised index, 100 = average weekday) ─────────────────
# These represent relative daily order volumes, not real numbers.
BASELINES = {
    "QSR":    {"weekday": 100, "saturday": 145, "sunday": 130},
    "Dine-in":{"weekday": 100, "saturday": 160, "sunday": 150},
    "PBCL":   {"weekday": 100, "saturday": 175, "sunday": 120},
}

# ── Event multipliers per restaurant type ─────────────────────────────────────
# Format: {category: {subcategory_or_"*": {restaurant_type: multiplier}}}
# Multiplier applies to the base index.
# Values > 1.0 = uplift, < 1.0 = suppression

EVENT_MULTIPLIERS = {
    "Festival": {
        "Hindu": {
            "QSR":    1.25,   # families eat out, quick bites spike
            "Dine-in":1.40,   # festive dining, celebrations
            "PBCL":   1.10,   # some uplift, but family-focused
        },
        "Muslim": {
            "QSR":    1.15,   # Eid family outings
            "Dine-in":1.35,   # Eid celebrations, big gatherings
            "PBCL":   0.80,   # lower — conservative during Eid
        },
        "Regional": {
            "QSR":    1.20,
            "Dine-in":1.45,
            "PBCL":   1.05,
        },
        "*": {
            "QSR":    1.20,
            "Dine-in":1.38,
            "PBCL":   1.05,
        },
    },
    "Government Holiday": {
        "*": {
            "QSR":    1.10,   # leisure browsing
            "Dine-in":1.25,   # family lunch/dinner outings
            "PBCL":   1.30,   # daytime drinking / café use goes up
        },
    },
    "Sports Event": {
        "Cricket": {
            "QSR":    1.18,   # quick delivery during match
            "Dine-in":0.85,   # people stay home to watch
            "PBCL":   1.55,   # huge uplift — live screening, drinks
        },
        "Football": {
            "QSR":    1.12,
            "Dine-in":0.88,
            "PBCL":   1.40,
        },
        "*": {
            "QSR":    1.15,
            "Dine-in":0.90,
            "PBCL":   1.45,
        },
    },
    "Commercial Event": {
        "*": {
            "QSR":    1.08,   # mall traffic → QSR
            "Dine-in":1.12,   # shopping leads to dining
            "PBCL":   1.05,
        },
    },
    "Public Event": {
        "*": {
            "QSR":    1.15,   # crowd footfall
            "Dine-in":1.05,
            "PBCL":   1.10,
        },
    },
    "Government Order": {
        "*": {
            "QSR":    0.90,   # restrictions reduce footfall
            "Dine-in":0.80,
            "PBCL":   0.75,
        },
    },
    "Emergency Crisis": {
        "Heatwave": {
            "QSR":    0.75,   # outdoor footfall collapses
            "Dine-in":0.65,   # no one steps out in 45°C
            "PBCL":   0.70,
        },
        "Flood": {
            "QSR":    0.40,
            "Dine-in":0.30,
            "PBCL":   0.25,
        },
        "Cyclone": {
            "QSR":    0.35,
            "Dine-in":0.25,
            "PBCL":   0.20,
        },
        "Air Quality": {
            "QSR":    0.80,   # delivery still works
            "Dine-in":0.60,   # dine-in collapses
            "PBCL":   0.55,
        },
        "Severe Weather": {
            "QSR":    0.70,
            "Dine-in":0.55,
            "PBCL":   0.50,
        },
        "*": {
            "QSR":    0.65,
            "Dine-in":0.55,
            "PBCL":   0.50,
        },
    },
}

# ── Weather multipliers (from temperature / precipitation) ────────────────────
def weather_multiplier(rest_type: str, temp_max: float, precip_mm: float,
                       weather_code: int) -> tuple:
    """Returns (multiplier, reason_str)."""
    mult   = 1.0
    reason = []

    if temp_max is not None:
        if temp_max >= 44:
            m = {"QSR": 0.75, "Dine-in": 0.60, "PBCL": 0.65}[rest_type]
            mult *= m; reason.append(f"Extreme heat {temp_max}°C")
        elif temp_max >= 40:
            m = {"QSR": 0.88, "Dine-in": 0.78, "PBCL": 0.82}[rest_type]
            mult *= m; reason.append(f"High heat {temp_max}°C")
        elif temp_max <= 15:
            m = {"QSR": 1.05, "Dine-in": 1.12, "PBCL": 1.08}[rest_type]
            mult *= m; reason.append(f"Cool weather {temp_max}°C — cosy dining")

    if precip_mm is not None:
        if precip_mm >= 20:
            m = {"QSR": 1.15, "Dine-in": 0.55, "PBCL": 0.60}[rest_type]
            mult *= m
            reason.append(f"Heavy rain {precip_mm}mm — delivery↑ dine-in↓")
        elif precip_mm >= 5:
            m = {"QSR": 1.08, "Dine-in": 0.80, "PBCL": 0.75}[rest_type]
            mult *= m; reason.append(f"Rain {precip_mm}mm")

    if weather_code in (95, 96, 99):
        m = {"QSR": 1.10, "Dine-in": 0.45, "PBCL": 0.40}[rest_type]
        mult *= m; reason.append("Thunderstorm — delivery spike, dine-in crash")

    return round(mult, 3), "; ".join(reason) if reason else "Normal weather"


# ── Day-of-week baseline ──────────────────────────────────────────────────────
def get_base(rest_type: str, weekday: int) -> float:
    b = BASELINES[rest_type]
    if weekday == 5:   return b["saturday"]
    if weekday == 6:   return b["sunday"]
    return b["weekday"]


# ── Main prediction function ──────────────────────────────────────────────────
def predict_impact(
    city:         str,
    pred_date:    date,
    rest_type:    str,          # "QSR" | "Dine-in" | "PBCL"
    temp_max:     float = None,
    precip_mm:    float = None,
    weather_code: int   = None,
) -> dict:
    """
    Returns impact prediction for one restaurant type on one date in one city.
    """
    base = get_base(rest_type, pred_date.weekday())

    # Get all events active on this date for this city
    evts = []
    d_str = pred_date.isoformat()
    from datetime import date as dt_date
    d = dt_date.fromisoformat(d_str)
    for ev in EVENTS_DB:
        ev_s = dt_date.fromisoformat(ev["start_date"])
        ev_e = dt_date.fromisoformat(ev["end_date"])
        if not (ev_s <= d <= ev_e):
            continue
        if not _event_applies_to_geo(ev, city=city):
            continue
        evts.append(ev)

    # Compound event multipliers
    event_mult   = 1.0
    event_factors = []
    for ev in evts:
        cat    = ev["category"]
        subcat = ev.get("subcategory", "*")
        cat_m  = EVENT_MULTIPLIERS.get(cat, {})
        sub_m  = cat_m.get(subcat, cat_m.get("*", {}))
        m      = sub_m.get(rest_type, 1.0)
        event_mult   *= m
        direction = "↑" if m > 1.0 else ("↓" if m < 1.0 else "→")
        event_factors.append(
            f"{ev['name']} ({cat}) {direction}{round((m-1)*100):+.0f}%"
        )

    # Weather multiplier
    w_mult, w_reason = weather_multiplier(
        rest_type, temp_max, precip_mm, weather_code or 0
    )

    # Final prediction
    total_mult     = event_mult * w_mult
    predicted      = round(base * total_mult, 1)
    pct_change     = round((total_mult - 1) * 100, 1)

    # Confidence
    if len(evts) == 0 and w_mult == 1.0:
        confidence = "High"
    elif abs(pct_change) > 40:
        confidence = "Low"
    elif abs(pct_change) > 20:
        confidence = "Medium"
    else:
        confidence = "High"

    # Overall signal
    if pct_change >= 30:      signal = "very_high_up"
    elif pct_change >= 15:    signal = "high_up"
    elif pct_change >= 5:     signal = "slight_up"
    elif pct_change <= -35:   signal = "very_low"
    elif pct_change <= -20:   signal = "low"
    elif pct_change <= -8:    signal = "slight_down"
    else:                     signal = "neutral"

    all_factors = event_factors + ([w_reason] if w_reason != "Normal weather" else [])

    return {
        "date":            d_str,
        "city":            city,
        "restaurant_type": rest_type,
        "weekday":         pred_date.strftime("%A"),
        "base_index":      base,
        "event_multiplier":round(event_mult, 3),
        "weather_multiplier": w_mult,
        "total_multiplier":round(total_mult, 3),
        "predicted_index": predicted,
        "pct_change":      pct_change,
        "signal":          signal,
        "confidence":      confidence,
        "active_events":   [e["name"] for e in evts],
        "factors":         all_factors,
        "weather_note":    w_reason,
    }


def predict_date_range(
    city:      str,
    start_dt:  date,
    end_dt:    date,
    temp_data: dict = None,   # {date_str: {"temp_max_c":..,"precipitation_mm":..,"weather_code":..}}
) -> dict:
    """
    Predict impact for all 3 restaurant types across a date range.
    Returns nested dict: {rest_type: [list of daily predictions]}
    """
    results = {"QSR": [], "Dine-in": [], "PBCL": []}
    cur = start_dt
    while cur <= end_dt:
        d_str  = cur.isoformat()
        td     = (temp_data or {}).get(d_str, {})
        tmax   = td.get("temp_max_c")
        precip = td.get("precipitation_mm")
        wcode  = td.get("weather_code")
        for rt in ["QSR", "Dine-in", "PBCL"]:
            results[rt].append(predict_impact(city, cur, rt, tmax, precip, wcode))
        cur += timedelta(days=1)
    return results
