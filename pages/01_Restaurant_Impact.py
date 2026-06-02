"""
Restaurant Impact Page — QSR, Dine-in, PBCL
Streamlit multi-page: place in pages/ folder next to dashboard.py
"""

import streamlit as st
import sys, os
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from data.india_geo import CITIES
from utils.restaurant_impact import predict_date_range, BASELINES

st.set_page_config(page_title="Restaurant Impact", page_icon="🍽️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.rt-card{border-radius:16px;padding:16px 20px;color:white;margin-bottom:12px;border-left:4px solid}
.sig-badge{display:inline-block;padding:4px 12px;border-radius:16px;font-size:12px;font-weight:600;margin-top:6px}
.kpi-big{text-align:center;background:rgba(255,255,255,.08);border-radius:14px;
  padding:16px 10px;border:1px solid rgba(255,255,255,.12);color:white}
.kpi-val{font-size:28px;font-weight:600}
.kpi-lbl{font-size:11px;opacity:.6;margin-top:4px}
.section-hdr{color:white;font-size:15px;font-weight:600;margin:18px 0 10px;
  padding-bottom:5px;border-bottom:1px solid rgba(255,255,255,.12)}
section[data-testid="stSidebar"]{background:rgba(13,27,42,.97)!important}
section[data-testid="stSidebar"] *{color:white!important}
</style>
""", unsafe_allow_html=True)

RT_COLORS = {"QSR":"#FF6F00","Dine-in":"#1565C0","PBCL":"#4A148C"}
RT_ICONS  = {"QSR":"🍔","Dine-in":"🍽️","PBCL":"🍺"}
RT_DESC   = {
    "QSR":    "Quick Service — counter orders, delivery, takeaway (e.g. Mad Over Donuts, 99 Pancakes)",
    "Dine-in":"Full Service — table dining, casual to fine dining restaurants",
    "PBCL":   "Pub, Bar, Café, Lounge — beverages + light bites (e.g. Barista, brewpubs)",
}
SIGNAL_COLOR = {
    "very_high_up":"#00C853","high_up":"#43A047","slight_up":"#81C784",
    "neutral":"#78909C","slight_down":"#FF8A65","low":"#EF5350","very_low":"#B71C1C",
}
SIGNAL_LABEL = {
    "very_high_up":"🚀 Very High","high_up":"📈 High Uplift","slight_up":"↑ Slight Uplift",
    "neutral":"➡️ Neutral","slight_down":"↓ Slight Drop","low":"📉 Low","very_low":"🔴 Very Low",
}

with st.sidebar:
    st.markdown("## 🍽️ Restaurant Impact")
    st.markdown("Predicted order volume vs normal baseline (100 = avg weekday)")
    st.markdown("---")
    city = st.selectbox("📍 City", sorted(CITIES.keys()),
                        index=sorted(CITIES.keys()).index("New Delhi"))
    st.markdown("---")
    today = date.today()
    c1,c2 = st.columns(2)
    with c1: start_date = st.date_input("From", today)
    with c2: end_date   = st.date_input("To",   today+timedelta(days=30))
    st.markdown("---")
    st.markdown("### 🌡️ Weather Override")
    override = st.toggle("Apply custom weather")
    temp_max  = st.slider("Max Temp (°C)", 10, 50, 32) if override else None
    precip_mm = st.slider("Rainfall (mm)", 0, 80, 0)   if override else None
    st.markdown("---")
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear(); st.rerun()

@st.cache_data(ttl=3600, show_spinner=False)
def get_weather(city, start_str, end_str):
    import requests
    coords = CITIES[city]; temp_map = {}; today = date.today()
    try:
        hist_end = min(date.fromisoformat(end_str), today - timedelta(days=1))
        if date.fromisoformat(start_str) <= hist_end:
            r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
                "latitude":coords["lat"],"longitude":coords["lon"],
                "daily":["temperature_2m_max","precipitation_sum","weathercode"],
                "start_date":start_str,"end_date":hist_end.isoformat(),"timezone":"Asia/Kolkata",
            }, timeout=12)
            if r.status_code == 200:
                d = r.json()["daily"]
                for i in range(len(d["time"])):
                    temp_map[d["time"][i]] = {"temp_max_c":d["temperature_2m_max"][i],
                        "precipitation_mm":d["precipitation_sum"][i],"weather_code":d["weathercode"][i]}
        fcst_start = max(date.fromisoformat(start_str), today)
        if fcst_start <= date.fromisoformat(end_str):
            days = (date.fromisoformat(end_str)-today).days+2
            r2 = requests.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude":coords["lat"],"longitude":coords["lon"],
                "daily":["temperature_2m_max","precipitation_sum","weathercode"],
                "forecast_days":min(days,16),"timezone":"Asia/Kolkata",
            }, timeout=10)
            if r2.status_code == 200:
                d2 = r2.json()["daily"]
                for i in range(len(d2["time"])):
                    temp_map[d2["time"][i]] = {"temp_max_c":d2["temperature_2m_max"][i],
                        "precipitation_mm":d2["precipitation_sum"][i],"weather_code":d2["weathercode"][i]}
    except: pass
    return temp_map

with st.spinner("Calculating impact..."):
    weather_data = get_weather(city, start_date.isoformat(), end_date.isoformat())
    if override:
        for k in weather_data: weather_data[k]["temp_max_c"]=temp_max; weather_data[k]["precipitation_mm"]=precip_mm
    predictions = predict_date_range(city, start_date, end_date, weather_data)

st.markdown(f"## 🍽️ Restaurant Demand Impact — {city}")
st.markdown(f"*{start_date.strftime('%d %b %Y')} → {end_date.strftime('%d %b %Y')} · Index: 100 = typical weekday*")

k1,k2,k3 = st.columns(3)
for col,rt in zip([k1,k2,k3],["QSR","Dine-in","PBCL"]):
    preds = predictions[rt]
    avg_i = sum(p["predicted_index"] for p in preds)/len(preds) if preds else 100
    avg_p = sum(p["pct_change"] for p in preds)/len(preds) if preds else 0
    best  = max(preds,key=lambda x:x["pct_change"]) if preds else {}
    worst = min(preds,key=lambda x:x["pct_change"]) if preds else {}
    c = RT_COLORS[rt]
    with col:
        st.markdown(f"""
        <div class="kpi-big" style="border-top:3px solid {c}">
          <div style="font-size:20px;margin-bottom:6px">{RT_ICONS[rt]} {rt}</div>
          <div class="kpi-val" style="color:{c}">{avg_i:.0f}</div>
          <div class="kpi-lbl">Avg predicted index</div>
          <div style="font-size:13px;margin-top:6px;color:{'#43A047' if avg_p>=0 else '#EF5350'};font-weight:500">
            {avg_p:+.1f}% vs baseline
          </div>
          <div style="font-size:10px;opacity:.4;margin-top:10px">
            Peak: {best.get('date','')[:10]} ({best.get('pct_change',0):+.0f}%)<br>
            Low:  {worst.get('date','')[:10]} ({worst.get('pct_change',0):+.0f}%)
          </div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1,tab2,tab3,tab4 = st.tabs(["🍔 QSR","🍽️ Dine-in","🍺 PBCL","📊 Compare All"])

def render_tab(rt):
    preds = predictions[rt]; c = RT_COLORS[rt]
    st.markdown(f"<div style='color:rgba(255,255,255,.5);font-size:12px;margin-bottom:12px'>{RT_DESC[rt]}</div>",unsafe_allow_html=True)
    try:
        import plotly.graph_objects as go
        dates=[p["date"] for p in preds]; idx=[p["predicted_index"] for p in preds]
        base=[p["base_index"] for p in preds]; pct=[p["pct_change"] for p in preds]
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=dates,y=base,name="Baseline",
            line=dict(color="rgba(255,255,255,.2)",width=1.5,dash="dot")))
        fig.add_trace(go.Scatter(x=dates,y=idx,name="Predicted",
            line=dict(color=c,width=2.5),fill="tonexty",
            fillcolor=f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},.12)",
            mode="lines+markers",marker=dict(size=6,color=c)))
        fig.add_trace(go.Bar(x=dates,y=pct,name="% Change",
            marker_color=[SIGNAL_COLOR.get(p["signal"],"#78909C") for p in preds],
            opacity=0.6,yaxis="y2"))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,.03)",
            font=dict(color="white",family="Inter"),height=300,margin=dict(l=0,r=0,t=10,b=0),
            hovermode="x unified",
            legend=dict(orientation="h",yanchor="bottom",y=1.02,bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,.08)",tickfont=dict(color="rgba(255,255,255,.6)")),
            yaxis=dict(title="Order Index",gridcolor="rgba(255,255,255,.08)",
                       tickfont=dict(color="rgba(255,255,255,.6)"),range=[0,260]),
            yaxis2=dict(title="% Change",overlaying="y",side="right",
                        tickfont=dict(color="rgba(255,255,255,.4)"),showgrid=False,
                        zeroline=True,zerolinecolor="rgba(255,255,255,.2)"))
        st.plotly_chart(fig,use_container_width=True)
    except Exception as e: st.info(f"Chart: {e}")

    st.markdown('<div class="section-hdr">Notable Impact Days (±8% or more)</div>',unsafe_allow_html=True)
    notable=[p for p in preds if abs(p["pct_change"])>=8]
    if notable:
        c1,c2=st.columns(2)
        for i,p in enumerate(notable):
            col=c1 if i%2==0 else c2
            sc=SIGNAL_COLOR.get(p["signal"],"#78909C"); sl=SIGNAL_LABEL.get(p["signal"])
            facts="<br>".join([f"• {f}" for f in p["factors"]]) if p["factors"] else "No major factors"
            with col:
                st.markdown(f"""
                <div class="rt-card" style="background:{c}18;border-left-color:{c}">
                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                      <div style="font-size:14px;font-weight:600">{p['weekday']}, {p['date']}</div>
                      <div class="sig-badge" style="background:{sc}22;border:1px solid {sc};color:{sc}">{sl}</div>
                    </div>
                    <div style="text-align:right">
                      <div style="font-size:26px;font-weight:300;color:{sc}">{p['pct_change']:+.0f}%</div>
                      <div style="font-size:12px;opacity:.5">Index: {p['predicted_index']:.0f}</div>
                    </div>
                  </div>
                  <div style="margin-top:8px;font-size:11px;opacity:.65;line-height:1.7">{facts}</div>
                  <div style="font-size:10px;opacity:.35;margin-top:5px">Confidence: {p['confidence']} · {len(p['active_events'])} event(s)</div>
                </div>""",unsafe_allow_html=True)
    else:
        st.info("No significant impact days in this date range. Try extending the range.")

with tab1: render_tab("QSR")
with tab2: render_tab("Dine-in")
with tab3: render_tab("PBCL")

with tab4:
    st.markdown("**All 3 restaurant types on one chart + impact heatmap + event table**")
    try:
        import plotly.graph_objects as go
        dates=[p["date"] for p in predictions["QSR"]]
        fig3=go.Figure()
        for rt in ["QSR","Dine-in","PBCL"]:
            idx=[p["predicted_index"] for p in predictions[rt]]
            fig3.add_trace(go.Scatter(x=dates,y=idx,name=f"{RT_ICONS[rt]} {rt}",
                line=dict(color=RT_COLORS[rt],width=2.5),mode="lines+markers",marker=dict(size=5)))
        fig3.add_hline(y=100,line_dash="dot",line_color="rgba(255,255,255,.2)",
                       annotation_text="Weekday baseline",annotation_font_color="rgba(255,255,255,.35)")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,.03)",
            font=dict(color="white",family="Inter"),height=320,margin=dict(l=0,r=0,t=10,b=0),
            hovermode="x unified",
            legend=dict(orientation="h",yanchor="bottom",y=1.02,bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,.08)",tickfont=dict(color="rgba(255,255,255,.6)")),
            yaxis=dict(title="Order Index (100=baseline)",gridcolor="rgba(255,255,255,.08)",
                       tickfont=dict(color="rgba(255,255,255,.6)")))
        st.plotly_chart(fig3,use_container_width=True)

        # Heatmap
        st.markdown('<div class="section-hdr">📅 Signal Heatmap</div>',unsafe_allow_html=True)
        sig_val={"very_high_up":3,"high_up":2,"slight_up":1,"neutral":0,"slight_down":-1,"low":-2,"very_low":-3}
        z_data=[]; y_labels=[]
        for rt in ["QSR","Dine-in","PBCL"]:
            z_data.append([sig_val.get(p["signal"],0) for p in predictions[rt]])
            y_labels.append(f"{RT_ICONS[rt]} {rt}")
        fig4=go.Figure(go.Heatmap(z=z_data,x=dates,y=y_labels,
            colorscale=[[0,"#B71C1C"],[0.17,"#EF5350"],[0.33,"#FF8A65"],
                        [0.5,"#455A64"],[0.67,"#81C784"],[0.83,"#43A047"],[1,"#00C853"]],
            zmin=-3,zmax=3,hoverongaps=False,showscale=True,
            colorbar=dict(title="Impact",tickvals=[-3,-2,-1,0,1,2,3],
                ticktext=["Very Low","Low","Slight↓","Neutral","Slight↑","High","Very High"],
                tickfont=dict(color="white",size=10),titlefont=dict(color="white"))))
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white",family="Inter"),height=200,margin=dict(l=0,r=0,t=10,b=0),
            xaxis=dict(tickfont=dict(color="rgba(255,255,255,.6)"),gridcolor="rgba(255,255,255,.05)"),
            yaxis=dict(tickfont=dict(color="rgba(255,255,255,.8)")))
        st.plotly_chart(fig4,use_container_width=True)
    except Exception as e: st.warning(f"Chart: {e}")

    # Event table
    st.markdown('<div class="section-hdr">📋 Event Impact Reference Table</div>',unsafe_allow_html=True)
    from data.events_db import EVENTS_DB, _event_applies_to_geo
    from datetime import date as dt_date
    from utils.restaurant_impact import EVENT_MULTIPLIERS
    active_evts=[]
    s=dt_date.fromisoformat(start_date.isoformat()); e=dt_date.fromisoformat(end_date.isoformat())
    for ev in EVENTS_DB:
        ev_s=dt_date.fromisoformat(ev["start_date"]); ev_e=dt_date.fromisoformat(ev["end_date"])
        if ev_e<s or ev_s>e: continue
        if not _event_applies_to_geo(ev,city=city): continue
        active_evts.append(ev)
    if active_evts:
        rows=[]
        for ev in active_evts:
            cat=ev["category"]; sub=ev.get("subcategory","*")
            cm=EVENT_MULTIPLIERS.get(cat,{}); sm=cm.get(sub,cm.get("*",{}))
            rows.append({"Event":ev["name"],"Category":cat,"Dates":f"{ev['start_date']} → {ev['end_date']}",
                "🍔 QSR":f"{(sm.get('QSR',1.0)-1)*100:+.0f}%",
                "🍽️ Dine-in":f"{(sm.get('Dine-in',1.0)-1)*100:+.0f}%",
                "🍺 PBCL":f"{(sm.get('PBCL',1.0)-1)*100:+.0f}%"})
        import pandas as pd
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    else: st.info("No events for this city and date range.")

st.markdown("---")
st.markdown("<div style='font-size:10px;color:rgba(255,255,255,.3)'>Order index: 100 = typical weekday. Sat baseline: QSR 145, Dine-in 160, PBCL 175. Sun: QSR 130, Dine-in 150, PBCL 120. Multipliers from industry benchmarks. Predictive model — actual results may vary.</div>",unsafe_allow_html=True)
