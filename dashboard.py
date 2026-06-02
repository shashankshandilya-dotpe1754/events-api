"""
India Events & Weather Dashboard — Self-Contained Version
=========================================================
Works on Streamlit Cloud with NO separate API server needed.
- Weather: calls Open-Meteo directly
- Events: reads events_db.py directly
Run: streamlit run dashboard.py
"""

import streamlit as st
import requests
import sys
import os
from datetime import date, timedelta, datetime
import pytz

# ── Path setup ─────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from data.india_geo import CITIES, ZONES
from data.events_db import EVENTS_DB, _event_applies_to_geo

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Events & Weather",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Open-Meteo ─────────────────────────────────────────────────────────────────
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL  = "https://archive-api.open-meteo.com/v1/archive"

WMO_EMOJI = {
    0:("☀️","Clear Sky"),      1:("🌤️","Mainly Clear"),  2:("⛅","Partly Cloudy"),
    3:("☁️","Overcast"),       45:("🌫️","Fog"),           48:("🌫️","Icy Fog"),
    51:("🌦️","Light Drizzle"),53:("🌧️","Drizzle"),       55:("🌧️","Heavy Drizzle"),
    61:("🌧️","Light Rain"),   63:("🌧️","Moderate Rain"), 65:("🌧️","Heavy Rain"),
    80:("🌦️","Showers"),      81:("🌧️","Showers"),       82:("⛈️","Violent Showers"),
    95:("⛈️","Thunderstorm"), 96:("⛈️","Thunderstorm"),  99:("⛈️","Severe Storm"),
}

def wmo(code):
    return WMO_EMOJI.get(code, ("🌡️","Unknown"))

@st.cache_data(ttl=900, show_spinner=False)
def get_forecast(city):
    coords = CITIES.get(city, {})
    if not coords: return []
    try:
        r = requests.get(FORECAST_URL, params={
            "latitude": coords["lat"], "longitude": coords["lon"],
            "daily": ["temperature_2m_max","temperature_2m_min",
                      "precipitation_sum","weathercode","precipitation_probability_max"],
            "forecast_days": 8, "timezone": "Asia/Kolkata",
        }, timeout=10)
        if r.status_code != 200: return []
        d = r.json()["daily"]
        return [{"date": d["time"][i],
                 "temp_max_c": d["temperature_2m_max"][i],
                 "temp_min_c": d["temperature_2m_min"][i],
                 "precipitation_mm": d["precipitation_sum"][i] or 0,
                 "rain_probability_pct": d["precipitation_probability_max"][i],
                 "weather_code": d["weathercode"][i],
                 } for i in range(len(d["time"]))]
    except: return []

@st.cache_data(ttl=3600, show_spinner=False)
def get_historical(city, days_back=30):
    coords = CITIES.get(city, {})
    if not coords: return []
    today    = date.today()
    start_dt = (today - timedelta(days=days_back)).isoformat()
    end_dt   = today.isoformat()          # include today so archive covers it
    try:
        r = requests.get(ARCHIVE_URL, params={
            "latitude": coords["lat"], "longitude": coords["lon"],
            "daily": ["temperature_2m_max","temperature_2m_min",
                      "precipitation_sum","weathercode"],
            "start_date": start_dt, "end_date": end_dt,
            "timezone": "Asia/Kolkata",
        }, timeout=15)
        if r.status_code != 200: return []
        d = r.json()["daily"]
        return [{"date": d["time"][i],
                 "temp_max_c": d["temperature_2m_max"][i],
                 "temp_min_c": d["temperature_2m_min"][i],
                 "precipitation_mm": d["precipitation_sum"][i] or 0,
                 "weather_code": d["weathercode"][i],
                 } for i in range(len(d["time"]))]
    except: return []

def get_events(start_str, end_str, city=None, category=None):
    from datetime import date as dt_date
    s = dt_date.fromisoformat(start_str)
    e = dt_date.fromisoformat(end_str)
    out = []
    for ev in EVENTS_DB:
        ev_s = dt_date.fromisoformat(ev["start_date"])
        ev_e = dt_date.fromisoformat(ev["end_date"])
        if ev_e < s or ev_s > e: continue
        if category and category != "All" and ev["category"] != category: continue
        if city and not _event_applies_to_geo(ev, city=city): continue
        out.append(ev)
    return out

def get_today_context(city):
    today_str = date.today().isoformat()
    evts = get_events(today_str, today_str, city=city)
    flags = {
        "has_festival":         any(e["category"]=="Festival" for e in evts),
        "has_gov_holiday":      any(e["category"]=="Government Holiday" for e in evts),
        "has_sports_event":     any(e["category"]=="Sports Event" for e in evts),
        "has_commercial_event": any(e["category"]=="Commercial Event" for e in evts),
        "has_public_event":     any(e["category"]=="Public Event" for e in evts),
        "has_emergency_crisis": any(e["category"]=="Emergency Crisis" for e in evts),
        "is_weekend":           date.today().weekday() >= 5,
    }
    impacts = [e["impact_on_demand"] for e in evts]
    if   "very_low"    in impacts: signal = "very_low"
    elif "low"         in impacts: signal = "low"
    elif "very_high_up"in impacts: signal = "very_high_up"
    elif "high_up"     in impacts: signal = "high_up"
    elif "slight_up"   in impacts: signal = "slight_up"
    elif "slight_down" in impacts: signal = "slight_down"
    else:                          signal = "neutral"
    return {"events": evts, "flags": flags, "signal": signal}

# ── Style ──────────────────────────────────────────────────────────────────────
IMPACT_COLOR = {
    "very_high_up":"#00C853","high_up":"#43A047","slight_up":"#81C784",
    "neutral_positive":"#78909C","neutral":"#78909C","neutral_to_slight_down":"#FFB74D",
    "slight_down":"#FF8A65","low":"#EF5350","very_low":"#B71C1C",
}
IMPACT_LABEL = {
    "very_high_up":"🚀 Very High Demand","high_up":"📈 High Demand",
    "slight_up":"↑ Slight Uplift","neutral_positive":"➕ Neutral-Positive",
    "neutral":"➡️ Neutral","neutral_to_slight_down":"↘ Slight Suppression",
    "slight_down":"↓ Suppressed","low":"📉 Low Demand","very_low":"🔴 Very Low Demand",
}
CAT_EMOJI = {
    "Festival":"🎉","Government Holiday":"🏛️","Sports Event":"🏏",
    "Commercial Event":"🛒","Public Event":"📢",
    "Government Order":"📋","Emergency Crisis":"🚨",
}
CAT_COLOR = {
    "Festival":"#FF6F00","Government Holiday":"#1565C0","Sports Event":"#6A1B9A",
    "Commercial Event":"#00695C","Public Event":"#2E7D32",
    "Government Order":"#37474F","Emergency Crisis":"#B71C1C",
}

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.weather-hero{background:linear-gradient(135deg,rgba(255,255,255,.15),rgba(255,255,255,.05));
  border:1px solid rgba(255,255,255,.2);border-radius:24px;
  padding:28px 32px;color:white;margin-bottom:16px}
.weather-emoji{font-size:64px;line-height:1}
.weather-temp{font-size:68px;font-weight:300;line-height:1}
.weather-label{font-size:18px;opacity:.85;margin-top:4px}
.weather-city{font-size:26px;font-weight:600}
.weather-date{font-size:13px;opacity:.65;margin-top:2px}
.metric-mini{background:rgba(255,255,255,.1);border-radius:12px;padding:10px 14px;
  color:white;text-align:center;border:1px solid rgba(255,255,255,.15)}
.metric-mini .val{font-size:18px;font-weight:600}
.metric-mini .lbl{font-size:11px;opacity:.65;margin-top:2px}
.forecast-card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);
  border-radius:16px;padding:14px 8px;text-align:center;color:white}
.forecast-day{font-size:12px;font-weight:600;opacity:.8}
.forecast-emoji{font-size:28px;margin:8px 0}
.forecast-hi{font-size:17px;font-weight:600}
.forecast-lo{font-size:12px;opacity:.55}
.forecast-rain{font-size:11px;color:#90CAF9;margin-top:4px}
.event-card{border-radius:14px;padding:14px 16px;margin-bottom:10px;
  border-left:4px solid;color:white}
.event-name{font-size:14px;font-weight:600}
.event-dates{font-size:11px;opacity:.7;margin-top:2px}
.section-hdr{color:white;font-size:16px;font-weight:600;margin:20px 0 12px;
  padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,.12)}
.context-card{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);
  border-radius:16px;padding:18px 20px;color:white}
.signal-badge{display:inline-block;padding:5px 14px;border-radius:20px;
  font-size:13px;font-weight:600;margin-top:6px}
section[data-testid="stSidebar"]{background:rgba(13,27,42,.97)!important;
  border-right:1px solid rgba(255,255,255,.1)}
section[data-testid="stSidebar"] *{color:white!important}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌦️ India Events & Weather")
    st.markdown("---")
    city = st.selectbox("📍 Select City", sorted(CITIES.keys()),
                        index=sorted(CITIES.keys()).index("New Delhi"))
    st.markdown("---")
    st.markdown("### 📅 Date Range")
    IST = pytz.timezone("Asia/Kolkata")
    today = datetime.now(IST).date()
    c1,c2 = st.columns(2)
    with c1: start_date = st.date_input("From", today)
    with c2: end_date   = st.date_input("To",   today+timedelta(days=30))
    st.markdown("---")
    st.markdown("### 🏷️ Filter Events")
    cats = ["All","Festival","Government Holiday","Sports Event",
            "Commercial Event","Public Event","Government Order","Emergency Crisis"]
    selected_cat = st.selectbox("Category", cats)
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    st.markdown("---")
    st.success("✅ Self-contained mode")
    st.markdown(
        f"<div style='color:rgba(255,255,255,.5);font-size:11px'>"
        f"📦 {len(EVENTS_DB)} events in DB<br>IST: {datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d %b %Y %I:%M %p")}<br>Date: {today.strftime('%d %b %Y')}</div>",
        unsafe_allow_html=True)

# ── Fetch data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading weather & events..."):
    forecast  = get_forecast(city)
    hist_data = get_historical(city, days_back=30)
    today_ctx = get_today_context(city)

# Try forecast first, fall back to archive if today missing
today_w = next((f for f in forecast if f.get("date") == today.isoformat()), {})
if not today_w or today_w.get("temp_max_c") is None:
    # Use archive data for today (more reliable when it's already late IST)
    arch_today = next((h for h in hist_data if h.get("date") == today.isoformat()), {})
    if arch_today.get("temp_max_c") is not None:
        today_w = arch_today
        # Add rain probability from first forecast day if available
        if forecast:
            first_f = forecast[0]
            today_w["rain_probability_pct"] = first_f.get("rain_probability_pct", "--")

# ── HERO + CONTEXT ─────────────────────────────────────────────────────────────
col_hero, col_ctx = st.columns([1.4,1], gap="large")

with col_hero:
    code  = today_w.get("weather_code", 1)
    em,lb = wmo(code)
    tmax  = today_w.get("temp_max_c","--")
    tmin  = today_w.get("temp_min_c","--")
    prec  = today_w.get("precipitation_mm",0) or 0
    rain_p= today_w.get("rain_probability_pct","--")
    tmax_s= f"{tmax}°C" if tmax!="--" else "--"
    tmin_s= f"{tmin}°C" if tmin!="--" else "--"
    rain_h= f"&nbsp;|&nbsp; 🌧 {rain_p}%" if rain_p!="--" else ""
    st.markdown(f"""
    <div class="weather-hero">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div>
          <div class="weather-city">📍 {city}</div>
          <div class="weather-date">{today.strftime('%A, %d %B %Y')}</div>
          <div class="weather-temp">{f"{tmax}°" if tmax!="--" else "--"}</div>
          <div class="weather-label">{lb}</div>
          <div style="font-size:13px;opacity:.65;margin-top:6px">Low {tmin_s} &nbsp;|&nbsp; Precip {prec}mm{rain_h}</div>
        </div>
        <div class="weather-emoji">{em}</div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px">
        <div class="metric-mini"><div class="val">{tmax_s}</div><div class="lbl">Max Temp</div></div>
        <div class="metric-mini"><div class="val">{tmin_s}</div><div class="lbl">Min Temp</div></div>
        <div class="metric-mini"><div class="val">{prec}mm</div><div class="lbl">Rainfall</div></div>
        <div class="metric-mini"><div class="val">{rain_p}%</div><div class="lbl">Rain Prob</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

with col_ctx:
    sig    = today_ctx["signal"]
    flags  = today_ctx["flags"]
    evc    = len(today_ctx["events"])
    sigc   = IMPACT_COLOR.get(sig,"#78909C")
    sigl   = IMPACT_LABEL.get(sig,sig)
    fm     = {"has_festival":("🎉","Festival"),"has_gov_holiday":("🏛️","Holiday"),
              "has_sports_event":("🏏","Sports"),"has_commercial_event":("🛒","Commercial"),
              "has_public_event":("📢","Public"),"has_emergency_crisis":("🚨","Crisis"),
              "is_weekend":("📅","Weekend")}
    active = [f"{i} {l}" for k,(i,l) in fm.items() if flags.get(k)]
    badges = " &nbsp;".join(
        [f"<span style='background:rgba(255,255,255,.15);padding:3px 10px;border-radius:12px;font-size:11px'>{f}</span>"
         for f in active]
    ) if active else "<span style='opacity:.45;font-size:12px'>No special events today</span>"
    st.markdown(f"""
    <div class="context-card">
      <div style="font-size:15px;font-weight:600;margin-bottom:10px">📊 Today's Demand Context</div>
      <div style="font-size:12px;opacity:.6;margin-bottom:10px">{today.strftime('%A, %d %B %Y')} &nbsp;·&nbsp; {city}</div>
      <div class="signal-badge" style="background:{sigc}22;border:1px solid {sigc};color:{sigc}">{sigl}</div>
      <div style="margin-top:14px;font-size:11px;font-weight:500;opacity:.6;margin-bottom:8px">ACTIVE FACTORS</div>
      <div style="line-height:2">{badges}</div>
      <div style="margin-top:12px;font-size:12px;opacity:.5">{evc} event(s) active today</div>
    </div>""", unsafe_allow_html=True)

# ── 7-DAY FORECAST ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">🌤️ 7-Day Forecast</div>', unsafe_allow_html=True)
if forecast:
    cols = st.columns(min(len(forecast),8))
    for i,day in enumerate(forecast[:8]):
        with cols[i]:
            d     = date.fromisoformat(day["date"])
            dn    = "Today" if d==today else ("Tomorrow" if d==today+timedelta(1) else d.strftime("%a"))
            em2,_ = wmo(day.get("weather_code",1))
            hi    = day.get("temp_max_c","--")
            lo    = day.get("temp_min_c","--")
            rp    = day.get("rain_probability_pct")
            rs    = f"🌧 {rp}%" if rp is not None else ""
            lb2   = wmo(day.get("weather_code",1))[1]
            bdr   = "border:1.5px solid rgba(255,255,255,.5);" if d==today else ""
            st.markdown(f"""
            <div class="forecast-card" style="{bdr}">
              <div class="forecast-day">{dn}<br>{d.strftime('%d %b')}</div>
              <div class="forecast-emoji">{em2}</div>
              <div style="font-size:10px;opacity:.55;margin-bottom:4px">{lb2}</div>
              <div class="forecast-hi">{hi}°</div>
              <div class="forecast-lo">{lo}°</div>
              <div class="forecast-rain">{rs}</div>
            </div>""", unsafe_allow_html=True)
else:
    st.warning("⚠️ Weather data unavailable — Open-Meteo may be temporarily down.")

# ── EVENTS ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">📅 Events & Holidays</div>', unsafe_allow_html=True)
events = get_events(start_date.isoformat(), end_date.isoformat(),
                    city=city, category=selected_cat)
if events:
    c1,c2 = st.columns(2)
    for i,ev in enumerate(events):
        col   = c1 if i%2==0 else c2
        cat   = ev.get("category","")
        ico   = CAT_EMOJI.get(cat,"📌")
        color = CAT_COLOR.get(cat,"#546E7A")
        imp   = ev.get("impact_on_demand","neutral")
        impl  = IMPACT_LABEL.get(imp,imp)
        impc  = IMPACT_COLOR.get(imp,"#90A4AE")
        scope = ev.get("scope","").replace("_"," ").title()
        sd    = ev.get("start_date","")
        ed    = ev.get("end_date","")
        ds    = sd if sd==ed else f"{sd} → {ed}"
        desc  = ev.get("description","")
        dh    = f"<div style='font-size:11px;opacity:.5;margin-top:5px'>{desc[:80]}...</div>" if desc else ""
        with col:
            st.markdown(f"""
            <div class="event-card" style="background:{color}22;border-left-color:{color}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                  <div class="event-name">{ico} {ev.get('name','')}</div>
                  <div class="event-dates">📅 {ds} &nbsp;·&nbsp; 🌐 {scope}</div>
                </div>
                <span style="background:{color}33;border:1px solid {color}66;color:{color};
                  font-size:10px;padding:2px 8px;border-radius:10px;white-space:nowrap;
                  margin-left:8px">{cat}</span>
              </div>
              <div style="font-size:11px;color:{impc};margin-top:6px;font-weight:500">{impl}</div>
              {dh}
            </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:rgba(255,255,255,.05);border-radius:16px;padding:32px;
      text-align:center;color:rgba(255,255,255,.4)">
      📭 No events found for the selected filters and date range.
    </div>""", unsafe_allow_html=True)

# ── HISTORICAL CHART ───────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">📈 Historical Temperature — Last 30 Days</div>',
            unsafe_allow_html=True)
hist = hist_data  # already fetched above
if hist:
    try:
        import plotly.graph_objects as go
        dts  = [d["date"] for d in hist]
        maxh = [d.get("temp_max_c") for d in hist]
        minh = [d.get("temp_min_c") for d in hist]
        prch = [d.get("precipitation_mm",0) for d in hist]
        fig  = go.Figure()
        fig.add_trace(go.Scatter(x=dts,y=maxh,name="Max Temp (°C)",
            line=dict(color="#FF7043",width=2.5),
            fill="tozeroy",fillcolor="rgba(255,112,67,.1)"))
        fig.add_trace(go.Scatter(x=dts,y=minh,name="Min Temp (°C)",
            line=dict(color="#42A5F5",width=2),
            fill="tozeroy",fillcolor="rgba(66,165,245,.1)"))
        fig.add_trace(go.Bar(x=dts,y=prch,name="Rainfall (mm)",
            marker_color="rgba(100,181,246,.5)",yaxis="y2"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,.04)",
            font=dict(color="white",family="Inter"),height=280,
            margin=dict(l=0,r=0,t=10,b=0),hovermode="x unified",
            legend=dict(orientation="h",yanchor="bottom",y=1.02,bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,.08)",tickfont=dict(color="rgba(255,255,255,.6)")),
            yaxis=dict(title="Temperature (°C)",gridcolor="rgba(255,255,255,.08)",
                       tickfont=dict(color="rgba(255,255,255,.6)")),
            yaxis2=dict(title="Rainfall (mm)",overlaying="y",side="right",
                        tickfont=dict(color="rgba(100,181,246,.8)"),showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info(f"Chart unavailable: {e}")
else:
    st.info("Historical weather data unavailable.")

# ── UPCOMING TIMELINE ──────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">🔮 Upcoming 30-Day Event Timeline</div>',
            unsafe_allow_html=True)
upcoming = get_events(today.isoformat(),(today+timedelta(days=30)).isoformat(),city=city)
if upcoming:
    try:
        import plotly.graph_objects as go2
        fig2 = go2.Figure()
        seen = set()
        for ev in upcoming:
            cat   = ev.get("category","Other")
            color = CAT_COLOR.get(cat,"#546E7A")
            name  = ev["name"]
            ico   = CAT_EMOJI.get(cat,"📌")
            sd    = ev["start_date"]
            ed    = ev["end_date"]
            dur   = (date.fromisoformat(ed)-date.fromisoformat(sd)).days+1
            fig2.add_trace(go2.Bar(
                x=[dur],y=[f"{ico} {name[:35]}"],base=[sd],orientation="h",
                marker=dict(color=color,opacity=0.8),
                name=cat if cat not in seen else "",showlegend=(cat not in seen),
                hovertemplate=f"<b>{name}</b><br>{sd} → {ed}<br>{cat}<extra></extra>",
            ))
            seen.add(cat)
        fig2.add_vline(x=today.isoformat(),line_color="rgba(255,255,255,.5)",
                       line_dash="dash",line_width=1.5)
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,.03)",
            font=dict(color="white",family="Inter"),barmode="stack",
            height=max(200,len(upcoming)*38),margin=dict(l=0,r=0,t=10,b=0),
            xaxis=dict(type="date",gridcolor="rgba(255,255,255,.08)",
                       tickfont=dict(color="rgba(255,255,255,.6)")),
            yaxis=dict(gridcolor="rgba(255,255,255,.05)",
                       tickfont=dict(color="rgba(255,255,255,.8)",size=11)),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,
                        bgcolor="rgba(0,0,0,0)",font=dict(color="white",size=11)),
        )
        st.plotly_chart(fig2, use_container_width=True)
    except Exception:
        for ev in upcoming:
            cat  = ev.get("category","")
            ico  = CAT_EMOJI.get(cat,"📌")
            col  = CAT_COLOR.get(cat,"#546E7A")
            st.markdown(f"""
            <div style="background:{col}22;border-left:3px solid {col};
              border-radius:8px;padding:8px 14px;margin-bottom:6px;color:white;font-size:13px">
              {ico} <b>{ev['name']}</b> &nbsp;·&nbsp; {ev['start_date']}
            </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:rgba(255,255,255,.05);border-radius:16px;padding:24px;
      text-align:center;color:rgba(255,255,255,.4)">
      📭 No upcoming events in next 30 days for this city.
    </div>""", unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;color:rgba(255,255,255,.25);font-size:11px;
  margin-top:32px;padding-top:16px;border-top:1px solid rgba(255,255,255,.08)">
  🌦️ India Events & Weather Dashboard &nbsp;·&nbsp; Weather: Open-Meteo (no API key)
  &nbsp;·&nbsp; {len(EVENTS_DB)} events in database &nbsp;·&nbsp; {city}
</div>""", unsafe_allow_html=True)
