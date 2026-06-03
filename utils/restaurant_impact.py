"""
restaurant_impact.py
====================
Hypothetical order volume impact model for 5 restaurant types:
  QSR           — Quick Service (Mad Over Donuts, 99 Pancakes, McDonald's)
  Fine Dining   — Full Service, upscale table dining
  PBCL          — Pub, Bar, Café, Lounge (Barista, brewpubs)
  Casual Dining — Mid-range sit-down (Chili's, Barbeque Nation)
  Cloud Kitchen — Delivery-only (Rebel Foods, Biryani By Kilo, Faasos)
  Cafe          — Coffee shops, bakery-cafes (Starbucks, Blue Tokai, Third Wave)

Each restaurant type responds differently to the same event/weather.
"""

from datetime import date, timedelta
from data.events_db import EVENTS_DB, _event_applies_to_geo

# ── Baseline orders (index, 100 = average weekday) ────────────────────────────
BASELINES = {
    "QSR":           {"weekday": 100, "saturday": 145, "sunday": 130},
    "Fine Dining":   {"weekday": 100, "saturday": 165, "sunday": 155},
    "PBCL":          {"weekday": 100, "saturday": 175, "sunday": 120},
    "Casual Dining": {"weekday": 100, "saturday": 155, "sunday": 145},
    "Cloud Kitchen": {"weekday": 100, "saturday": 130, "sunday": 125},
    "Cafe":          {"weekday": 100, "saturday": 140, "sunday": 135},
}

ALL_RT = list(BASELINES.keys())

# ── Event multipliers per restaurant type ─────────────────────────────────────
EVENT_MULTIPLIERS = {
    "Festival": {
        "Hindu": {
            "QSR":           1.25,
            "Fine Dining":   1.45,
            "PBCL":          1.10,
            "Casual Dining": 1.35,
            "Cloud Kitchen": 1.20,
            "Cafe":          1.15,
        },
        "Muslim": {
            "QSR":           1.15,
            "Fine Dining":   1.40,
            "PBCL":          0.75,
            "Casual Dining": 1.30,
            "Cloud Kitchen": 1.25,
            "Cafe":          1.05,
        },
        "Regional": {
            "QSR":           1.20,
            "Fine Dining":   1.50,
            "PBCL":          1.05,
            "Casual Dining": 1.38,
            "Cloud Kitchen": 1.18,
            "Cafe":          1.12,
        },
        "*": {
            "QSR":           1.20,
            "Fine Dining":   1.42,
            "PBCL":          1.05,
            "Casual Dining": 1.35,
            "Cloud Kitchen": 1.18,
            "Cafe":          1.12,
        },
    },
    "Government Holiday": {
        "*": {
            "QSR":           1.10,
            "Fine Dining":   1.30,
            "PBCL":          1.35,
            "Casual Dining": 1.25,
            "Cloud Kitchen": 1.15,
            "Cafe":          1.20,
        },
    },
    "Sports Event": {
        "Cricket": {
            "QSR":           1.18,
            "Fine Dining":   0.80,
            "PBCL":          1.55,
            "Casual Dining": 0.90,
            "Cloud Kitchen": 1.45,  # big delivery spike during IPL/WC
            "Cafe":          1.10,
        },
        "Football": {
            "QSR":           1.12,
            "Fine Dining":   0.85,
            "PBCL":          1.40,
            "Casual Dining": 0.92,
            "Cloud Kitchen": 1.35,
            "Cafe":          1.08,
        },
        "*": {
            "QSR":           1.15,
            "Fine Dining":   0.85,
            "PBCL":          1.45,
            "Casual Dining": 0.92,
            "Cloud Kitchen": 1.38,
            "Cafe":          1.08,
        },
    },
    "Commercial Event": {
        "*": {
            "QSR":           1.08,
            "Fine Dining":   1.15,
            "PBCL":          1.05,
            "Casual Dining": 1.12,
            "Cloud Kitchen": 1.05,
            "Cafe":          1.10,
        },
    },
    "Public Event": {
        "*": {
            "QSR":           1.15,
            "Fine Dining":   1.05,
            "PBCL":          1.10,
            "Casual Dining": 1.08,
            "Cloud Kitchen": 1.10,
            "Cafe":          1.12,
        },
    },
    "Government Order": {
        "*": {
            "QSR":           0.90,
            "Fine Dining":   0.75,
            "PBCL":          0.70,
            "Casual Dining": 0.80,
            "Cloud Kitchen": 0.95,
            "Cafe":          0.85,
        },
    },
    "Emergency Crisis": {
        "Heatwave": {
            "QSR":           0.75,
            "Fine Dining":   0.60,
            "PBCL":          0.65,
            "Casual Dining": 0.65,
            "Cloud Kitchen": 0.85,  # delivery still works
            "Cafe":          0.70,
        },
        "Flood": {
            "QSR":           0.40,
            "Fine Dining":   0.25,
            "PBCL":          0.20,
            "Casual Dining": 0.30,
            "Cloud Kitchen": 0.50,
            "Cafe":          0.35,
        },
        "Cyclone": {
            "QSR":           0.35,
            "Fine Dining":   0.20,
            "PBCL":          0.15,
            "Casual Dining": 0.25,
            "Cloud Kitchen": 0.40,
            "Cafe":          0.30,
        },
        "Air Quality": {
            "QSR":           0.78,
            "Fine Dining":   0.55,
            "PBCL":          0.50,
            "Casual Dining": 0.62,
            "Cloud Kitchen": 0.90,
            "Cafe":          0.65,
        },
        "Severe Weather": {
            "QSR":           0.70,
            "Fine Dining":   0.50,
            "PBCL":          0.45,
            "Casual Dining": 0.58,
            "Cloud Kitchen": 0.80,
            "Cafe":          0.60,
        },
        "*": {
            "QSR":           0.65,
            "Fine Dining":   0.50,
            "PBCL":          0.45,
            "Casual Dining": 0.55,
            "Cloud Kitchen": 0.78,
            "Cafe":          0.58,
        },
    },
}

# ── Weather multipliers ────────────────────────────────────────────────────────
def weather_multiplier(rest_type: str, temp_max: float, precip_mm: float,
                       weather_code: int) -> tuple:
    mult = 1.0; reason = []
    if temp_max is not None:
        if temp_max >= 44:
            m = {"QSR":0.75,"Fine Dining":0.58,"PBCL":0.62,
                 "Casual Dining":0.63,"Cloud Kitchen":0.85,"Cafe":0.68}[rest_type]
            mult *= m; reason.append(f"Extreme heat {temp_max}°C")
        elif temp_max >= 40:
            m = {"QSR":0.88,"Fine Dining":0.75,"PBCL":0.80,
                 "Casual Dining":0.80,"Cloud Kitchen":0.92,"Cafe":0.82}[rest_type]
            mult *= m; reason.append(f"High heat {temp_max}°C")
        elif temp_max <= 15:
            m = {"QSR":1.05,"Fine Dining":1.15,"PBCL":1.10,
                 "Casual Dining":1.12,"Cloud Kitchen":1.08,"Cafe":1.18}[rest_type]
            mult *= m; reason.append(f"Cool {temp_max}°C — cosy dining")
    if precip_mm is not None:
        if precip_mm >= 20:
            m = {"QSR":1.15,"Fine Dining":0.50,"PBCL":0.55,
                 "Casual Dining":0.60,"Cloud Kitchen":1.40,"Cafe":0.72}[rest_type]
            mult *= m; reason.append(f"Heavy rain {precip_mm}mm")
        elif precip_mm >= 5:
            m = {"QSR":1.08,"Fine Dining":0.78,"PBCL":0.72,
                 "Casual Dining":0.80,"Cloud Kitchen":1.20,"Cafe":0.85}[rest_type]
            mult *= m; reason.append(f"Rain {precip_mm}mm")
    if weather_code in (95,96,99):
        m = {"QSR":1.10,"Fine Dining":0.42,"PBCL":0.38,
             "Casual Dining":0.50,"Cloud Kitchen":1.35,"Cafe":0.55}[rest_type]
        mult *= m; reason.append("Thunderstorm")
    return round(mult, 3), "; ".join(reason) if reason else "Normal weather"


def get_base(rest_type: str, weekday: int) -> float:
    b = BASELINES[rest_type]
    if weekday == 5: return b["saturday"]
    if weekday == 6: return b["sunday"]
    return b["weekday"]


def predict_impact(city, pred_date, rest_type,
                   temp_max=None, precip_mm=None, weather_code=None):
    base = get_base(rest_type, pred_date.weekday())
    evts = []
    from datetime import date as dt_date
    d = dt_date.fromisoformat(pred_date.isoformat())
    for ev in EVENTS_DB:
        ev_s = dt_date.fromisoformat(ev["start_date"])
        ev_e = dt_date.fromisoformat(ev["end_date"])
        if not (ev_s <= d <= ev_e): continue
        if not _event_applies_to_geo(ev, city=city): continue
        evts.append(ev)

    event_mult = 1.0; event_factors = []
    for ev in evts:
        cat = ev["category"]; subcat = ev.get("subcategory","*")
        cat_m = EVENT_MULTIPLIERS.get(cat,{})
        sub_m = cat_m.get(subcat, cat_m.get("*",{}))
        m = sub_m.get(rest_type, 1.0)
        event_mult *= m
        direction = "↑" if m>1.0 else ("↓" if m<1.0 else "→")
        event_factors.append(f"{ev['name']} ({cat}) {direction}{round((m-1)*100):+.0f}%")

    w_mult, w_reason = weather_multiplier(rest_type, temp_max, precip_mm, weather_code or 0)
    total_mult  = event_mult * w_mult
    predicted   = round(base * total_mult, 1)
    pct_change  = round((total_mult - 1) * 100, 1)

    if   pct_change >= 30:   signal = "very_high_up"
    elif pct_change >= 15:   signal = "high_up"
    elif pct_change >= 5:    signal = "slight_up"
    elif pct_change <= -35:  signal = "very_low"
    elif pct_change <= -20:  signal = "low"
    elif pct_change <= -8:   signal = "slight_down"
    else:                    signal = "neutral"

    if   len(evts)==0 and w_mult==1.0: confidence="High"
    elif abs(pct_change)>40:           confidence="Low"
    elif abs(pct_change)>20:           confidence="Medium"
    else:                              confidence="High"

    all_factors = event_factors + ([w_reason] if w_reason!="Normal weather" else [])
    return {
        "date": pred_date.isoformat(), "city": city,
        "restaurant_type": rest_type,
        "weekday": pred_date.strftime("%A"),
        "base_index": base, "event_multiplier": round(event_mult,3),
        "weather_multiplier": w_mult, "total_multiplier": round(total_mult,3),
        "predicted_index": predicted, "pct_change": pct_change,
        "signal": signal, "confidence": confidence,
        "active_events": [e["name"] for e in evts],
        "factors": all_factors, "weather_note": w_reason,
    }


def predict_date_range(city, start_dt, end_dt, temp_data=None):
    results = {rt: [] for rt in ALL_RT}
    cur = start_dt
    while cur <= end_dt:
        d_str = cur.isoformat()
        td    = (temp_data or {}).get(d_str, {})
        for rt in ALL_RT:
            results[rt].append(predict_impact(
                city, cur, rt,
                td.get("temp_max_c"), td.get("precipitation_mm"), td.get("weather_code")
            ))
        cur += timedelta(days=1)
    return results
