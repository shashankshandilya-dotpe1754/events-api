"""
India Events & Weather Dashboard
Run: streamlit run dashboard.py
Requires the Events API running at http://localhost:8000
"""

import streamlit as st
import requests
from datetime import date, timedelta
import json

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Events & Weather",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000"

# ── WMO weather code → emoji + label ─────────────────────────────────────────
WMO_EMOJI = {
    0: ("☀️", "Clear Sky"),      1: ("🌤️", "Mainly Clear"),
    2: ("⛅", "Partly Cloudy"),  3: ("☁️", "Overcast"),
    45: ("🌫️", "Fog"),           48: ("🌫️", "Icy Fog"),
    51: ("🌦️", "Light Drizzle"), 53: ("🌧️", "Drizzle"),     55: ("🌧️", "Heavy Drizzle"),
    61: ("🌧️", "Light Rain"),   63: ("🌧️", "Moderate Rain"), 65: ("🌧️", "Heavy Rain"),
    71: ("🌨️", "Light Snow"),   73: ("❄️", "Snow"),          75: ("❄️", "Heavy Snow"),
    80: ("🌦️", "Showers"),      81: ("🌧️", "Showers"),      82: ("⛈️", "Violent Showers"),
    95: ("⛈️", "Thunderstorm"), 96: ("⛈️", "Thunderstorm"), 99: ("⛈️", "Severe Storm"),
}

IMPACT_COLOR = {
    "very_high_up":             "#00C853",
    "high_up":                  "#43A047",
    "slight_up":                "#81C784",
    "neutral_positive":         "#B0BEC5",
    "neutral":                  "#B0BEC5",
    "neutral_to_slight_down":   "#FFB74D",
    "slight_down":              "#FF8A65",
    "low":                      "#EF5350",
    "very_low":                 "#B71C1C",
}

IMPACT_LABEL = {
    "very_high_up":             "🚀 Very High Demand",
    "high_up":                  "📈 High Demand",
    "slight_up":                "↑ Slight Uplift",
    "neutral_positive":         "➕ Neutral-Positive",
    "neutral":                  "➡️ Neutral",
    "neutral_to_slight_down":   "↘ Slight Suppression",
    "slight_down":              "↓ Suppressed",
    "low":                      "📉 Low Demand",
    "very_low":                 "🔴 Very Low Demand",
}

CAT_EMOJI = {
    "Festival":           "🎉",
    "Government Holiday": "🏛️",
    "Sports Event":       "🏏",
    "Commercial Event":   "🛒",
    "Public Event":       "📢",
    "Government Order":   "📋",
    "Emergency Crisis":   "🚨",
}

CAT_COLOR = {
    "Festival":           "#FF6F00",
    "Government Holiday": "#1565C0",
    "Sports Event":       "#6A1B9A",
    "Commercial Event":   "#00695C",
    "Public Event":       "#2E7D32",
    "Government Order":   "#37474F",
    "Emergency Crisis":   "#B71C1C",
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Main background */
.main { background: linear-gradient(135deg, #0D1B2A 0%, #1B2A4A 50%, #0D1B2A 100%); }

/* Weather hero card */
.weather-hero {
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 24px;
    padding: 28px 32px;
    color: white;
    margin-bottom: 16px;
}
.weather-temp { font-size: 72px; font-weight: 300; line-height: 1; }
.weather-emoji { font-size: 64px; }
.weather-label { font-size: 18px; font-weight: 400; opacity: 0.85; margin-top: 4px; }
.weather-city { font-size: 28px; font-weight: 600; }
.weather-date { font-size: 13px; opacity: 0.7; margin-top: 2px; }

/* Metric mini card */
.metric-mini {
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 10px 14px;
    color: white;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.15);
}
.metric-mini .val { font-size: 20px; font-weight: 600; }
.metric-mini .lbl { font-size: 11px; opacity: 0.7; margin-top: 2px; }

/* Forecast card */
.forecast-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 14px 10px;
    text-align: center;
    color: white;
    transition: transform .2s;
}
.forecast-card:hover { transform: translateY(-3px); }
.forecast-day { font-size: 12px; font-weight: 600; opacity: 0.8; }
.forecast-emoji { font-size: 30px; margin: 8px 0; }
.forecast-hi { font-size: 18px; font-weight: 600; }
.forecast-lo { font-size: 13px; opacity: 0.6; }
.forecast-rain { font-size: 11px; color: #90CAF9; margin-top: 4px; }

/* Event card */
.event-card {
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
    border-left: 4px solid;
    color: white;
}
.event-name { font-size: 14px; font-weight: 600; }
.event-dates { font-size: 11px; opacity: 0.75; margin-top: 2px; }
.event-impact { font-size: 11px; margin-top: 6px; font-weight: 500; }

/* Section header */
.section-hdr {
    color: white;
    font-size: 16px;
    font-weight: 600;
    margin: 20px 0 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}

/* Today context card */
.context-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 16px 20px;
    color: white;
    margin-bottom: 12px;
}

/* Signal badge */
.signal-badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 6px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(13,27,42,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=900)
def fetch_forecast(city):
    try:
        r = requests.get(f"{API_BASE}/weather/city/{city}/forecast", params={"days": 8}, timeout=10)
        if r.status_code == 200:
            return r.json().get("daily", [])
    except:
        pass
    return []

@st.cache_data(ttl=900)
def fetch_events_range(start, end, city=None):
    try:
        params = {"start_date": start, "end_date": end}
        if city:
            params["city"] = city
        r = requests.get(f"{API_BASE}/events/range", params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get("events", [])
    except:
        pass
    return []

@st.cache_data(ttl=300)
def fetch_day_context(date_str, city):
    try:
        r = requests.get(f"{API_BASE}/calendar/{date_str}", params={"city": city}, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {}

@st.cache_data(ttl=3600)
def fetch_cities():
    try:
        r = requests.get(f"{API_BASE}/geo/cities", timeout=5)
        if r.status_code == 200:
            return list(r.json().get("cities", {}).keys())
    except:
        pass
    return ["New Delhi","Mumbai","Bengaluru","Hyderabad","Navi Mumbai","Jaipur","Ludhiana"]

def wmo(code):
    return WMO_EMOJI.get(code, ("🌡️", "Unknown"))


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌦️ India Events & Weather")
    st.markdown("---")

    cities = fetch_cities()
    city = st.selectbox("📍 Select City", cities,
                        index=cities.index("New Delhi") if "New Delhi" in cities else 0)

    st.markdown("---")
    st.markdown("### 📅 Date Range")
    today = date.today()
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", today)
    with col2:
        end_date   = st.date_input("To", today + timedelta(days=30))

    st.markdown("---")
    st.markdown("### 🏷️ Filter Events")
    categories = ["All", "Festival", "Government Holiday", "Sports Event",
                  "Commercial Event", "Public Event", "Government Order", "Emergency Crisis"]
    selected_cat = st.selectbox("Category", categories)

    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    # API Status
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        if r.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")

    st.markdown(f"<div style='color:rgba(255,255,255,0.4);font-size:11px;margin-top:8px'>Today: {today.strftime('%d %b %Y')}</div>", unsafe_allow_html=True)


# ── Main content ──────────────────────────────────────────────────────────────
forecast = fetch_forecast(city)
today_ctx = fetch_day_context(today.isoformat(), city)
today_weather = today_ctx.get("weather", {}) or {}

# Get today's data from forecast if calendar weather missing
if not today_weather and forecast:
    today_weather = next((f for f in forecast if f.get("date") == today.isoformat()), {})

# ── TOP ROW: Weather Hero + Today Context ─────────────────────────────────────
col_hero, col_ctx = st.columns([1.4, 1], gap="large")

with col_hero:
    code  = today_weather.get("weather_code", 1)
    emoji, label = wmo(code)
    tmax  = today_weather.get("temp_max_c", "--")
    tmin  = today_weather.get("temp_min_c", "--")
    prec  = today_weather.get("precipitation_mm", 0) or 0
    rain_p = today_weather.get("rain_probability_pct", "--")

    st.markdown(f"""
    <div class="weather-hero">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
                <div class="weather-city">📍 {city}</div>
                <div class="weather-date">{today.strftime('%A, %d %B %Y')}</div>
                <div class="weather-temp">{tmax}°</div>
                <div class="weather-label">{label}</div>
                <div style="font-size:13px;opacity:0.7;margin-top:6px">
                    Low {tmin}°C &nbsp;|&nbsp; Precip {prec}mm
                    {"&nbsp;|&nbsp; 🌧 " + str(rain_p) + "%" if rain_p != "--" else ""}
                </div>
            </div>
            <div class="weather-emoji">{emoji}</div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px">
            <div class="metric-mini"><div class="val">{tmax}°C</div><div class="lbl">Max Temp</div></div>
            <div class="metric-mini"><div class="val">{tmin}°C</div><div class="lbl">Min Temp</div></div>
            <div class="metric-mini"><div class="val">{prec}mm</div><div class="lbl">Rainfall</div></div>
            <div class="metric-mini"><div class="val">{rain_p}%</div><div class="lbl">Rain Prob</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_ctx:
    signal   = today_ctx.get("overall_demand_signal", "neutral")
    flags    = today_ctx.get("summary_flags", {})
    ev_count = today_ctx.get("event_count", 0)
    sig_color = IMPACT_COLOR.get(signal, "#90A4AE")
    sig_label = IMPACT_LABEL.get(signal, signal)

    active_flags = []
    flag_map = {
        "has_festival":         ("🎉", "Festival"),
        "has_gov_holiday":      ("🏛️", "Holiday"),
        "has_sports_event":     ("🏏", "Sports"),
        "has_commercial_event": ("🛒", "Commercial"),
        "has_public_event":     ("📢", "Public Event"),
        "has_emergency_crisis": ("🚨", "Crisis"),
        "is_weekend":           ("📅", "Weekend"),
    }
    for key, (ico, lbl) in flag_map.items():
        if flags.get(key):
            active_flags.append(f"{ico} {lbl}")

    flags_html = " &nbsp; ".join([f"<span style='background:rgba(255,255,255,0.15);padding:3px 10px;border-radius:12px;font-size:12px'>{f}</span>" for f in active_flags]) if active_flags else "<span style='opacity:0.5;font-size:12px'>No special events today</span>"

    st.markdown(f"""
    <div class="context-card" style="height:100%">
        <div style="font-size:15px;font-weight:600;margin-bottom:10px">📊 Today's Demand Context</div>
        <div style="font-size:13px;opacity:0.7;margin-bottom:8px">{today.strftime('%A, %d %B %Y')} &nbsp;·&nbsp; {city}</div>
        <div class="signal-badge" style="background:{sig_color}22;border:1px solid {sig_color};color:{sig_color}">
            {sig_label}
        </div>
        <div style="margin-top:14px;font-size:12px;font-weight:500;opacity:0.7;margin-bottom:8px">ACTIVE FACTORS</div>
        <div>{flags_html}</div>
        <div style="margin-top:14px;font-size:12px;opacity:0.6">{ev_count} event(s) active today</div>
    </div>
    """, unsafe_allow_html=True)


# ── 7-DAY FORECAST ────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">🌤️ 7-Day Forecast</div>', unsafe_allow_html=True)

if forecast:
    fcols = st.columns(min(len(forecast), 8))
    for i, day in enumerate(forecast[:8]):
        with fcols[i]:
            d     = date.fromisoformat(day["date"])
            day_name = "Today" if d == today else ("Tomorrow" if d == today + timedelta(1) else d.strftime("%a"))
            code  = day.get("weather_code", 1)
            em, lb = wmo(code)
            hi    = day.get("temp_max_c", "--")
            lo    = day.get("temp_min_c", "--")
            rp    = day.get("rain_probability_pct")
            rain_str = f"🌧 {rp}%" if rp is not None else ""
            is_today = "border: 1.5px solid rgba(255,255,255,0.5);" if d == today else ""
            st.markdown(f"""
            <div class="forecast-card" style="{is_today}">
                <div class="forecast-day">{day_name}<br>{d.strftime('%d %b')}</div>
                <div class="forecast-emoji">{em}</div>
                <div style="font-size:10px;opacity:0.6;margin-bottom:4px">{lb}</div>
                <div class="forecast-hi">{hi}°</div>
                <div class="forecast-lo">{lo}°</div>
                <div class="forecast-rain">{rain_str}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Weather forecast unavailable. Check API connection.")


# ── EVENTS SECTION ────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">📅 Events & Holidays</div>', unsafe_allow_html=True)

events = fetch_events_range(start_date.isoformat(), end_date.isoformat(), city)
if selected_cat != "All":
    events = [e for e in events if e["category"] == selected_cat]

if events:
    col_ev1, col_ev2 = st.columns(2)
    for i, ev in enumerate(events):
        col = col_ev1 if i % 2 == 0 else col_ev2
        cat   = ev.get("category", "")
        ico   = CAT_EMOJI.get(cat, "📌")
        color = CAT_COLOR.get(cat, "#546E7A")
        imp   = ev.get("impact_on_demand", "neutral")
        imp_lbl = IMPACT_LABEL.get(imp, imp)
        imp_col = IMPACT_COLOR.get(imp, "#90A4AE")
        scope = ev.get("scope", "").replace("_", " ").title()
        start = ev.get("start_date", "")
        end_e = ev.get("end_date", "")
        date_str = start if start == end_e else f"{start} → {end_e}"

        with col:
            st.markdown(f"""
            <div class="event-card" style="background:{color}22;border-left-color:{color}">
                <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div>
                        <div class="event-name">{ico} {ev.get('name','')}</div>
                        <div class="event-dates">📅 {date_str} &nbsp;·&nbsp; 🌐 {scope}</div>
                    </div>
                    <span style="background:{color}33;border:1px solid {color}66;color:{color};
                        font-size:10px;padding:2px 8px;border-radius:10px;white-space:nowrap;margin-left:8px">
                        {cat}
                    </span>
                </div>
                <div class="event-impact" style="color:{imp_col}">{imp_lbl}</div>
                {"<div style='font-size:11px;opacity:0.6;margin-top:4px'>" + ev.get('description','')[:80] + "...</div>" if ev.get('description') else ""}
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);border-radius:16px;padding:32px;text-align:center;color:rgba(255,255,255,0.5)">
        📭 No events found for the selected filters and date range.
    </div>
    """, unsafe_allow_html=True)


# ── HISTORICAL WEATHER CHART ──────────────────────────────────────────────────
st.markdown('<div class="section-hdr">📈 Historical Temperature Trend</div>', unsafe_allow_html=True)

try:
    import plotly.graph_objects as go
    hist_start = (today - timedelta(days=30)).isoformat()
    hist_end   = (today - timedelta(days=1)).isoformat()
    r = requests.get(f"{API_BASE}/weather/city/{city}/historical",
                     params={"start_date": hist_start, "end_date": hist_end}, timeout=15)
    if r.status_code == 200:
        hist = r.json().get("daily", [])
        dates_h = [d["date"] for d in hist if "date" in d]
        max_h   = [d.get("temp_max_c") for d in hist if "date" in d]
        min_h   = [d.get("temp_min_c") for d in hist if "date" in d]
        prec_h  = [d.get("precipitation_mm", 0) or 0 for d in hist if "date" in d]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates_h, y=max_h, name="Max Temp (°C)",
            line=dict(color="#FF7043", width=2.5),
            fill="tozeroy", fillcolor="rgba(255,112,67,0.1)",
        ))
        fig.add_trace(go.Scatter(
            x=dates_h, y=min_h, name="Min Temp (°C)",
            line=dict(color="#42A5F5", width=2),
            fill="tozeroy", fillcolor="rgba(66,165,245,0.1)",
        ))
        fig.add_trace(go.Bar(
            x=dates_h, y=prec_h, name="Rainfall (mm)",
            marker_color="rgba(100,181,246,0.5)",
            yaxis="y2",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.04)",
            font=dict(color="white", family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font=dict(color="white")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="rgba(255,255,255,0.6)")),
            yaxis=dict(title="Temperature (°C)", gridcolor="rgba(255,255,255,0.08)",
                       tickfont=dict(color="rgba(255,255,255,0.6)")),
            yaxis2=dict(title="Rainfall (mm)", overlaying="y", side="right",
                        tickfont=dict(color="rgba(100,181,246,0.8)"), showgrid=False),
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.info(f"Historical chart: {e}")


# ── UPCOMING EVENTS TIMELINE ──────────────────────────────────────────────────
st.markdown('<div class="section-hdr">🔮 Upcoming 30-Day Event Timeline</div>', unsafe_allow_html=True)

upcoming = fetch_events_range(today.isoformat(), (today + timedelta(days=30)).isoformat(), city)
if upcoming:
    try:
        import plotly.figure_factory as ff
        import plotly.graph_objects as go2

        fig2 = go2.Figure()
        colors_used = {}
        y_vals = list(range(len(upcoming)))

        for i, ev in enumerate(upcoming):
            cat   = ev.get("category", "Other")
            color = CAT_COLOR.get(cat, "#546E7A")
            s     = ev["start_date"]
            e_d   = ev["end_date"]
            name  = ev["name"]
            ico   = CAT_EMOJI.get(cat, "📌")

            # Duration bar
            fig2.add_trace(go2.Bar(
                x=[(date.fromisoformat(e_d) - date.fromisoformat(s)).days + 1],
                y=[f"{ico} {name[:30]}"],
                base=[s],
                orientation="h",
                marker=dict(color=color, opacity=0.8),
                name=cat if cat not in colors_used else "",
                showlegend=(cat not in colors_used),
                hovertemplate=f"<b>{name}</b><br>{s} → {e_d}<br>{cat}<extra></extra>",
            ))
            colors_used[cat] = True

        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(color="white", family="Inter"),
            barmode="stack",
            xaxis=dict(
                type="date",
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(color="rgba(255,255,255,0.6)"),
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.05)",
                tickfont=dict(color="rgba(255,255,255,0.8)", size=11),
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font=dict(color="white", size=11)),
            height=max(200, len(upcoming) * 36),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        # Today line
        fig2.add_vline(x=today.isoformat(), line_color="rgba(255,255,255,0.4)",
                       line_dash="dash", line_width=1.5)
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        for ev in upcoming[:10]:
            cat   = ev.get("category", "")
            ico   = CAT_EMOJI.get(cat, "📌")
            color = CAT_COLOR.get(cat, "#546E7A")
            st.markdown(f"""
            <div style="background:{color}22;border-left:3px solid {color};
                border-radius:8px;padding:8px 14px;margin-bottom:6px;color:white;font-size:13px">
                {ico} <b>{ev['name']}</b> &nbsp;·&nbsp; {ev['start_date']}
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);border-radius:16px;padding:24px;
        text-align:center;color:rgba(255,255,255,0.5)">
        📭 No upcoming events in next 30 days for this city.
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:rgba(255,255,255,0.3);font-size:11px;margin-top:32px;padding-top:16px;
    border-top:1px solid rgba(255,255,255,0.08)">
    🌦️ India Events & Weather API &nbsp;·&nbsp; Weather: Open-Meteo &nbsp;·&nbsp;
    Events: Centralized API &nbsp;·&nbsp; Auto-refreshes every 15 min
</div>
""", unsafe_allow_html=True)
