"""
Master events database for India (Apr 2023 – present + future).
Schema per event:
  id, category, subcategory, name, start_date, end_date,
  scope (pan_india / zone / state / city),
  zones[], states[], cities[],
  description, impact_on_demand, source, tags[]
"""

from datetime import date

EVENTS_DB = [

    # ══════════════════════════════════════════════════════════════════
    # GOVERNMENT HOLIDAYS — Pan India (Gazetted)
    # ══════════════════════════════════════════════════════════════════
    {"id":"GH001","category":"Government Holiday","subcategory":"National Holiday","name":"Independence Day","start_date":"2023-08-15","end_date":"2023-08-15","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"National holiday — 77th Independence Day","impact_on_demand":"neutral_to_slight_up","source":"GoI","tags":["national","patriotic"]},
    {"id":"GH002","category":"Government Holiday","subcategory":"National Holiday","name":"Gandhi Jayanti","start_date":"2023-10-02","end_date":"2023-10-02","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Birth anniversary of Mahatma Gandhi","impact_on_demand":"neutral","source":"GoI","tags":["national"]},
    {"id":"GH003","category":"Government Holiday","subcategory":"National Holiday","name":"Republic Day","start_date":"2024-01-26","end_date":"2024-01-26","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"75th Republic Day","impact_on_demand":"neutral_to_slight_up","source":"GoI","tags":["national"]},
    {"id":"GH004","category":"Government Holiday","subcategory":"National Holiday","name":"Independence Day","start_date":"2024-08-15","end_date":"2024-08-15","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"78th Independence Day","impact_on_demand":"neutral_to_slight_up","source":"GoI","tags":["national"]},
    {"id":"GH005","category":"Government Holiday","subcategory":"National Holiday","name":"Gandhi Jayanti","start_date":"2024-10-02","end_date":"2024-10-02","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Gandhi Jayanti 2024","impact_on_demand":"neutral","source":"GoI","tags":["national"]},
    {"id":"GH006","category":"Government Holiday","subcategory":"National Holiday","name":"Republic Day","start_date":"2025-01-26","end_date":"2025-01-26","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"76th Republic Day","impact_on_demand":"neutral_to_slight_up","source":"GoI","tags":["national"]},
    {"id":"GH007","category":"Government Holiday","subcategory":"National Holiday","name":"Labour Day / Maharashtra Day","start_date":"2025-05-01","end_date":"2025-05-01","scope":"state","zones":["West","South","East"],"states":["Maharashtra","West Bengal","Tamil Nadu","Kerala","Telangana","Karnataka"],"cities":[],"description":"International Workers Day / Maharashtra Statehood Day","impact_on_demand":"low","source":"State Govts","tags":["labour","closure"]},
    {"id":"GH008","category":"Government Holiday","subcategory":"National Holiday","name":"Independence Day","start_date":"2025-08-15","end_date":"2025-08-15","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"79th Independence Day","impact_on_demand":"neutral_to_slight_up","source":"GoI","tags":["national"]},
    {"id":"GH009","category":"Government Holiday","subcategory":"National Holiday","name":"Gandhi Jayanti","start_date":"2025-10-02","end_date":"2025-10-02","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Gandhi Jayanti 2025","impact_on_demand":"neutral","source":"GoI","tags":["national"]},
    {"id":"GH010","category":"Government Holiday","subcategory":"National Holiday","name":"Republic Day","start_date":"2026-01-26","end_date":"2026-01-26","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"77th Republic Day 2026","impact_on_demand":"neutral_to_slight_up","source":"GoI","tags":["national"]},
    {"id":"GH011","category":"Government Holiday","subcategory":"National Holiday","name":"Labour Day 2026","start_date":"2026-05-01","end_date":"2026-05-01","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"International Workers Day 2026","impact_on_demand":"low","source":"GoI","tags":["closure"]},

    # ══════════════════════════════════════════════════════════════════
    # FESTIVALS
    # ══════════════════════════════════════════════════════════════════
    # 2023
    {"id":"FE001","category":"Festival","subcategory":"Hindu","name":"Navratri 2023","start_date":"2023-10-15","end_date":"2023-10-24","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"9-night festival; high footfall at malls/restaurants in Gujarat, Delhi, Mumbai","impact_on_demand":"high_up","source":"Religious calendar","tags":["navratri","garba","festive_season"]},
    {"id":"FE002","category":"Festival","subcategory":"Hindu","name":"Dussehra 2023","start_date":"2023-10-24","end_date":"2023-10-24","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Vijaya Dashami — holiday in most states","impact_on_demand":"slight_up","source":"Religious calendar","tags":["dussehra"]},
    {"id":"FE003","category":"Festival","subcategory":"Hindu","name":"Diwali 2023","start_date":"2023-11-10","end_date":"2023-11-14","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Festival of lights — peak consumer spending, high dining footfall","impact_on_demand":"very_high_up","source":"Religious calendar","tags":["diwali","festive_season","peak"]},
    {"id":"FE004","category":"Festival","subcategory":"Hindu","name":"Holi 2024","start_date":"2024-03-25","end_date":"2024-03-25","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Festival of colours — high street footfall day-after","impact_on_demand":"slight_up","source":"Religious calendar","tags":["holi","spring"]},
    {"id":"FE005","category":"Festival","subcategory":"Hindu","name":"Ram Navami 2024","start_date":"2024-04-17","end_date":"2024-04-17","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Religious holiday — moderate impact","impact_on_demand":"neutral","source":"Religious calendar","tags":["ram_navami"]},
    {"id":"FE006","category":"Festival","subcategory":"Muslim","name":"Eid ul-Fitr 2024","start_date":"2024-04-10","end_date":"2024-04-11","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"End of Ramadan — high dining and gifting footfall","impact_on_demand":"high_up","source":"Islamic calendar","tags":["eid","ramadan"]},
    {"id":"FE007","category":"Festival","subcategory":"Hindu","name":"Navratri 2024","start_date":"2024-10-03","end_date":"2024-10-12","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Navratri 2024 — festive season begins","impact_on_demand":"high_up","source":"Religious calendar","tags":["navratri","garba","festive_season"]},
    {"id":"FE008","category":"Festival","subcategory":"Hindu","name":"Dussehra 2024","start_date":"2024-10-12","end_date":"2024-10-12","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Vijaya Dashami 2024","impact_on_demand":"slight_up","source":"Religious calendar","tags":["dussehra"]},
    {"id":"FE009","category":"Festival","subcategory":"Hindu","name":"Diwali 2024","start_date":"2024-10-31","end_date":"2024-11-03","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Diwali 2024 — peak festive spending","impact_on_demand":"very_high_up","source":"Religious calendar","tags":["diwali","peak","festive_season"]},
    {"id":"FE010","category":"Festival","subcategory":"Hindu","name":"Holi 2025","start_date":"2025-03-14","end_date":"2025-03-14","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Holi 2025 — street celebrations drive post-celebration dining","impact_on_demand":"slight_up","source":"Religious calendar","tags":["holi","spring"]},
    {"id":"FE011","category":"Festival","subcategory":"Hindu","name":"Baisakhi 2025","start_date":"2025-04-13","end_date":"2025-04-13","scope":"zone","zones":["North"],"states":["Punjab","Haryana","Delhi","Himachal Pradesh"],"cities":[],"description":"Harvest festival — high footfall in North India especially Punjab","impact_on_demand":"high_up","source":"Religious calendar","tags":["baisakhi","north_india","harvest"]},
    {"id":"FE012","category":"Festival","subcategory":"Muslim","name":"Eid ul-Fitr 2025","start_date":"2025-03-31","end_date":"2025-04-01","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"End of Ramadan 2025 — high footfall in Muslim-majority areas","impact_on_demand":"high_up","source":"Islamic calendar","tags":["eid","ramadan"]},
    {"id":"FE013","category":"Festival","subcategory":"Muslim","name":"Eid ul-Adha 2025","start_date":"2025-06-07","end_date":"2025-06-08","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Bakrid 2025 — family gatherings; moderate QSR impact","impact_on_demand":"slight_up","source":"Islamic calendar","tags":["eid_adha","bakrid"]},
    {"id":"FE014","category":"Festival","subcategory":"Hindu","name":"Navratri 2025","start_date":"2025-09-22","end_date":"2025-10-02","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Navratri 2025 — festive season opener","impact_on_demand":"high_up","source":"Religious calendar","tags":["navratri","festive_season"]},
    {"id":"FE015","category":"Festival","subcategory":"Hindu","name":"Diwali 2025","start_date":"2025-10-20","end_date":"2025-10-23","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Diwali 2025","impact_on_demand":"very_high_up","source":"Religious calendar","tags":["diwali","peak","festive_season"]},
    {"id":"FE016","category":"Festival","subcategory":"Hindu","name":"Holi 2026","start_date":"2026-03-03","end_date":"2026-03-03","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Holi 2026","impact_on_demand":"slight_up","source":"Religious calendar","tags":["holi","spring"]},
    {"id":"FE017","category":"Festival","subcategory":"Muslim","name":"Eid ul-Adha 2026","start_date":"2026-05-27","end_date":"2026-05-28","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Bakrid 2026 — Eid post-holiday dampening effect in June 2026","impact_on_demand":"neutral_to_slight_down","source":"Islamic calendar","tags":["eid_adha","bakrid"]},
    {"id":"FE018","category":"Festival","subcategory":"Regional","name":"Pongal 2024","start_date":"2024-01-14","end_date":"2024-01-17","scope":"zone","zones":["South"],"states":["Tamil Nadu","Andhra Pradesh","Telangana"],"cities":[],"description":"South Indian harvest festival — high dining footfall","impact_on_demand":"high_up","source":"Tamil calendar","tags":["pongal","south_india","harvest"]},
    {"id":"FE019","category":"Festival","subcategory":"Regional","name":"Onam 2024","start_date":"2024-09-15","end_date":"2024-09-15","scope":"zone","zones":["South"],"states":["Kerala"],"cities":[],"description":"Kerala harvest festival — highest footfall in Kerala","impact_on_demand":"very_high_up","source":"Malayalam calendar","tags":["onam","kerala","harvest"]},
    {"id":"FE020","category":"Festival","subcategory":"Regional","name":"Pongal 2025","start_date":"2025-01-14","end_date":"2025-01-17","scope":"zone","zones":["South"],"states":["Tamil Nadu","Andhra Pradesh","Telangana"],"cities":[],"description":"Pongal 2025","impact_on_demand":"high_up","source":"Tamil calendar","tags":["pongal","south_india"]},
    {"id":"FE021","category":"Festival","subcategory":"Regional","name":"Ganesh Chaturthi 2024","start_date":"2024-09-07","end_date":"2024-09-17","scope":"zone","zones":["West","South"],"states":["Maharashtra","Goa","Karnataka","Andhra Pradesh","Telangana"],"cities":[],"description":"11-day festival — very high Mumbai/Pune footfall","impact_on_demand":"high_up","source":"Hindu calendar","tags":["ganesh","maharashtra","festive"]},
    {"id":"FE022","category":"Festival","subcategory":"Regional","name":"Ganesh Chaturthi 2025","start_date":"2025-08-27","end_date":"2025-09-06","scope":"zone","zones":["West","South"],"states":["Maharashtra","Goa","Karnataka","Andhra Pradesh","Telangana"],"cities":[],"description":"Ganesh Chaturthi 2025","impact_on_demand":"high_up","source":"Hindu calendar","tags":["ganesh","maharashtra","festive"]},
    {"id":"FE023","category":"Festival","subcategory":"Hindu","name":"Durga Puja 2024","start_date":"2024-10-09","end_date":"2024-10-14","scope":"zone","zones":["East","North"],"states":["West Bengal","Bihar","Assam","Odisha","Delhi"],"cities":[],"description":"Peak festive event for East India — very high Kolkata dining footfall","impact_on_demand":"very_high_up","source":"Bengali calendar","tags":["durga_puja","kolkata","bengal"]},
    {"id":"FE024","category":"Festival","subcategory":"Hindu","name":"Durga Puja 2025","start_date":"2025-09-29","end_date":"2025-10-04","scope":"zone","zones":["East","North"],"states":["West Bengal","Bihar","Assam","Odisha","Delhi"],"cities":[],"description":"Durga Puja 2025","impact_on_demand":"very_high_up","source":"Bengali calendar","tags":["durga_puja","kolkata","bengal"]},

    # ══════════════════════════════════════════════════════════════════
    # PUBLIC EVENTS
    # ══════════════════════════════════════════════════════════════════
    {"id":"PE001","category":"Public Event","subcategory":"Political","name":"2024 General Elections","start_date":"2024-04-19","end_date":"2024-06-01","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Phase 1-7 of Lok Sabha elections 2024 — dry days, restricted movement on polling dates","impact_on_demand":"low","source":"ECI","tags":["elections","lok_sabha","dry_day"]},
    {"id":"PE002","category":"Public Event","subcategory":"Political","name":"Delhi Assembly Elections 2025","start_date":"2025-02-05","end_date":"2025-02-05","scope":"city","zones":["North"],"states":["Delhi"],"cities":["New Delhi"],"description":"Delhi Vidhan Sabha elections 2025 — dry day, restricted movement","impact_on_demand":"low","source":"ECI Delhi","tags":["elections","delhi","dry_day"]},
    {"id":"PE003","category":"Public Event","subcategory":"Civic","name":"India International Trade Fair 2023","start_date":"2023-11-14","end_date":"2023-11-27","scope":"city","zones":["North"],"states":["Delhi"],"cities":["New Delhi"],"description":"Annual IITF at Pragati Maidan — high footfall in New Delhi","impact_on_demand":"high_up","source":"ITPO","tags":["trade_fair","delhi","iitf"]},
    {"id":"PE004","category":"Public Event","subcategory":"Civic","name":"India International Trade Fair 2024","start_date":"2024-11-14","end_date":"2024-11-27","scope":"city","zones":["North"],"states":["Delhi"],"cities":["New Delhi"],"description":"IITF 2024 at Pragati Maidan","impact_on_demand":"high_up","source":"ITPO","tags":["trade_fair","delhi","iitf"]},

    # ══════════════════════════════════════════════════════════════════
    # COMMERCIAL EVENTS
    # ══════════════════════════════════════════════════════════════════
    {"id":"CE001","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Amazon Great Indian Festival 2023","start_date":"2023-10-07","end_date":"2023-10-11","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Amazon's festive season mega sale — drives mall/F&B footfall","impact_on_demand":"slight_up","source":"Amazon","tags":["amazon","sale","ecommerce","festive_season"]},
    {"id":"CE002","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Flipkart Big Billion Days 2023","start_date":"2023-10-08","end_date":"2023-10-12","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Flipkart's flagship festive sale","impact_on_demand":"slight_up","source":"Flipkart","tags":["flipkart","sale","ecommerce"]},
    {"id":"CE003","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Amazon Great Indian Festival 2024","start_date":"2024-09-27","end_date":"2024-10-06","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Amazon festive season sale 2024","impact_on_demand":"slight_up","source":"Amazon","tags":["amazon","sale","ecommerce"]},
    {"id":"CE004","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Flipkart Big Billion Days 2024","start_date":"2024-10-06","end_date":"2024-10-11","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Flipkart BBD 2024","impact_on_demand":"slight_up","source":"Flipkart","tags":["flipkart","sale","ecommerce"]},
    {"id":"CE005","category":"Commercial Event","subcategory":"F&B Promotion","name":"Zomato Hyperpure Fest 2024","start_date":"2024-03-01","end_date":"2024-03-31","scope":"city","zones":["North","West","South"],"states":["Delhi","Maharashtra","Karnataka","Telangana"],"cities":["New Delhi","Mumbai","Bengaluru","Hyderabad"],"description":"Zomato dining promotions — drives QSR orders","impact_on_demand":"slight_up","source":"Zomato","tags":["zomato","dining","qsr"]},
    {"id":"CE006","category":"Commercial Event","subcategory":"F&B Promotion","name":"Swiggy It 2024","start_date":"2024-07-01","end_date":"2024-07-07","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Swiggy week-long mega promotion — boosts app orders","impact_on_demand":"high_up","source":"Swiggy","tags":["swiggy","delivery","promotion"]},
    {"id":"CE007","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Amazon Great Indian Festival 2025","start_date":"2025-09-25","end_date":"2025-10-04","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Amazon festive sale 2025","impact_on_demand":"slight_up","source":"Amazon","tags":["amazon","sale","ecommerce"]},

    # ══════════════════════════════════════════════════════════════════
    # SPORTS EVENTS
    # ══════════════════════════════════════════════════════════════════
    {"id":"SP001","category":"Sports Event","subcategory":"Cricket","name":"IPL 2023","start_date":"2023-04-21","end_date":"2023-05-28","scope":"city","zones":["West","South","North","East"],"states":["Maharashtra","Karnataka","Telangana","Delhi","West Bengal","Punjab","Rajasthan","Gujarat"],"cities":["Mumbai","Bengaluru","Hyderabad","New Delhi","Kolkata","Ludhiana","Jaipur","Ahmedabad"],"description":"IPL 2023 — matches drive evening orders. Home team cities see strongest effect.","impact_on_demand":"slight_up","source":"BCCI","tags":["ipl","cricket","evening_spike"]},
    {"id":"SP002","category":"Sports Event","subcategory":"Cricket","name":"ODI World Cup 2023","start_date":"2023-10-05","end_date":"2023-11-19","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"ICC Men's ODI World Cup 2023 — hosted in India. Match evenings see delivery surge.","impact_on_demand":"high_up","source":"ICC/BCCI","tags":["world_cup","cricket","odi","delivery_surge"]},
    {"id":"SP003","category":"Sports Event","subcategory":"Cricket","name":"IPL 2024","start_date":"2024-03-22","end_date":"2024-05-26","scope":"city","zones":["West","South","North","East"],"states":["Maharashtra","Karnataka","Telangana","Delhi","West Bengal","Punjab","Rajasthan","Gujarat"],"cities":["Mumbai","Bengaluru","Hyderabad","New Delhi","Kolkata","Ludhiana","Jaipur","Ahmedabad"],"description":"IPL 2024 Season 17","impact_on_demand":"slight_up","source":"BCCI","tags":["ipl","cricket"]},
    {"id":"SP004","category":"Sports Event","subcategory":"Cricket","name":"T20 World Cup 2024","start_date":"2024-06-01","end_date":"2024-06-29","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"ICC T20 World Cup 2024 (USA & West Indies) — India matches drive late-night delivery spike","impact_on_demand":"high_up","source":"ICC","tags":["t20","world_cup","cricket"]},
    {"id":"SP005","category":"Sports Event","subcategory":"Cricket","name":"IPL 2025","start_date":"2025-03-22","end_date":"2025-05-25","scope":"city","zones":["West","South","North","East"],"states":["Maharashtra","Karnataka","Telangana","Delhi","West Bengal","Punjab","Rajasthan","Gujarat"],"cities":["Mumbai","Bengaluru","Hyderabad","New Delhi","Kolkata","Ludhiana","Jaipur","Ahmedabad"],"description":"IPL 2025 Season 18","impact_on_demand":"slight_up","source":"BCCI","tags":["ipl","cricket"]},
    {"id":"SP006","category":"Sports Event","subcategory":"Cricket","name":"Champions Trophy 2025","start_date":"2025-02-19","end_date":"2025-03-09","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"ICC Champions Trophy 2025 — India matches drive delivery surge","impact_on_demand":"high_up","source":"ICC","tags":["champions_trophy","cricket"]},
    {"id":"SP007","category":"Sports Event","subcategory":"Cricket","name":"IPL 2026","start_date":"2026-03-20","end_date":"2026-05-24","scope":"city","zones":["West","South","North","East"],"states":["Maharashtra","Karnataka","Telangana","Delhi","West Bengal","Punjab","Rajasthan","Gujarat"],"cities":["Mumbai","Bengaluru","Hyderabad","New Delhi","Kolkata","Ludhiana","Jaipur","Ahmedabad"],"description":"IPL 2026 Season 19 (projected dates)","impact_on_demand":"slight_up","source":"BCCI","tags":["ipl","cricket"]},
    {"id":"SP008","category":"Sports Event","subcategory":"Football","name":"ISL Season 2023-24","start_date":"2023-09-21","end_date":"2024-03-03","scope":"city","zones":["West","East","South"],"states":["Maharashtra","West Bengal","Kerala","Goa","Karnataka"],"cities":["Mumbai","Kolkata","Kochi","Goa","Bengaluru"],"description":"Indian Super League 2023-24 season","impact_on_demand":"neutral","source":"FSDL","tags":["isl","football"]},

    # ══════════════════════════════════════════════════════════════════
    # GOVERNMENT ORDERS / POLICY
    # ══════════════════════════════════════════════════════════════════
    {"id":"GO001","category":"Government Order","subcategory":"Food Safety","name":"FSSAI Hygiene Rating Mandate","start_date":"2024-01-01","end_date":"2024-12-31","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"FSSAI mandated hygiene rating display for all food businesses — compliance drives trust","impact_on_demand":"neutral_positive","source":"FSSAI","tags":["fssai","food_safety","compliance"]},
    {"id":"GO002","category":"Government Order","subcategory":"Taxation","name":"GST Rate Revision on Restaurant Services","start_date":"2023-07-01","end_date":"2023-12-31","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"GST Council reduced 5% → maintained for standalone restaurants; AC restaurants 18% remains","impact_on_demand":"neutral","source":"GST Council","tags":["gst","taxation","restaurant"]},
    {"id":"GO003","category":"Government Order","subcategory":"Digital Mandate","name":"ONDC QSR Integration Mandate","start_date":"2024-06-01","end_date":"2025-12-31","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"ONDC driving QSR brands onto open network — increases digital orders","impact_on_demand":"slight_up","source":"DPIIT / ONDC","tags":["ondc","digital","qsr","ecommerce"]},
    {"id":"GO004","category":"Government Order","subcategory":"Health","name":"Air Quality Emergency — Winter Smog Protocol","start_date":"2024-11-15","end_date":"2024-11-25","scope":"city","zones":["North"],"states":["Delhi","Haryana","Punjab","Uttar Pradesh"],"cities":["New Delhi","Noida","Ludhiana"],"description":"Air Quality Index > 400. Delhi Govt bans outdoor seating, restricts dine-in hours.","impact_on_demand":"low","source":"Delhi Govt / CPCB","tags":["aqi","smog","delhi","health","restrictions"]},
    {"id":"GO005","category":"Government Order","subcategory":"Health","name":"Cyclone Michaung — Coastal Emergency","start_date":"2023-12-04","end_date":"2023-12-06","scope":"city","zones":["South"],"states":["Andhra Pradesh","Tamil Nadu","Telangana"],"cities":["Chennai","Hyderabad","Visakhapatnam"],"description":"Cyclone Michaung made landfall near Chennai — state holiday, closures, restrictions","impact_on_demand":"very_low","source":"IMD / NDMA","tags":["cyclone","emergency","chennai","closure"]},

    # ══════════════════════════════════════════════════════════════════
    # EMERGENCY CRISIS
    # ══════════════════════════════════════════════════════════════════
    {"id":"EC001","category":"Emergency Crisis","subcategory":"Natural Disaster","name":"Cyclone Biparjoy 2023","start_date":"2023-06-12","end_date":"2023-06-16","scope":"zone","zones":["West"],"states":["Gujarat","Rajasthan"],"cities":["Ahmedabad","Surat","Jaipur"],"description":"Very severe cyclonic storm hit Gujarat coast — evacuations, closures, disrupted supply chain","impact_on_demand":"very_low","source":"IMD / NDMA","tags":["cyclone","gujarat","emergency","crisis"]},
    {"id":"EC002","category":"Emergency Crisis","subcategory":"Flood","name":"Delhi Floods 2023","start_date":"2023-07-13","end_date":"2023-07-18","scope":"city","zones":["North"],"states":["Delhi"],"cities":["New Delhi"],"description":"Yamuna river breached banks — parts of Old Delhi, Mayur Vihar flooded. Severe supply disruption.","impact_on_demand":"very_low","source":"Delhi Disaster Management Authority","tags":["flood","delhi","monsoon","crisis"]},
    {"id":"EC003","category":"Emergency Crisis","subcategory":"Heatwave","name":"North India Heatwave 2024","start_date":"2024-05-15","end_date":"2024-06-25","scope":"zone","zones":["North","Central"],"states":["Delhi","Uttar Pradesh","Haryana","Rajasthan","Madhya Pradesh","Bihar"],"cities":["New Delhi","Jaipur","Lucknow","Bhopal","Patna"],"description":"Extreme heat 45-50°C across North India — IMD red alert. Reduces outdoor footfall significantly.","impact_on_demand":"low","source":"IMD","tags":["heatwave","north_india","extreme_heat","crisis"]},
    {"id":"EC004","category":"Emergency Crisis","subcategory":"Flood","name":"Assam Floods 2024","start_date":"2024-06-16","end_date":"2024-07-10","scope":"zone","zones":["East","Northeast"],"states":["Assam","Arunachal Pradesh","Meghalaya"],"cities":["Guwahati"],"description":"Severe flooding — Brahmaputra basin. 40+ districts affected.","impact_on_demand":"very_low","source":"ASDMA","tags":["flood","assam","monsoon","crisis"]},
    {"id":"EC005","category":"Emergency Crisis","subcategory":"Heatwave","name":"North India Pre-Monsoon Heatwave 2025","start_date":"2025-05-15","end_date":"2025-06-10","scope":"zone","zones":["North","Central"],"states":["Delhi","Uttar Pradesh","Haryana","Rajasthan","Madhya Pradesh"],"cities":["New Delhi","Jaipur","Lucknow","Ludhiana"],"description":"IMD Red alert heatwave — temperature 43-47°C. Strong suppressor on outdoor footfall.","impact_on_demand":"low","source":"IMD","tags":["heatwave","north_india","extreme_heat","crisis"]},
    {"id":"EC006","category":"Emergency Crisis","subcategory":"Air Quality","name":"Winter Smog Emergency Delhi 2025","start_date":"2025-11-01","end_date":"2025-11-20","scope":"city","zones":["North"],"states":["Delhi","Haryana","Punjab"],"cities":["New Delhi","Ludhiana"],"description":"AQI > 450 — GRAP 4 restrictions, school closures, WFH advisory. Footfall suppressed.","impact_on_demand":"low","source":"CPCB / Delhi Govt","tags":["aqi","smog","delhi","crisis"]},
    {"id":"EC007","category":"Emergency Crisis","subcategory":"Cyclone","name":"Cyclone Fengal 2024","start_date":"2024-11-29","end_date":"2024-12-01","scope":"zone","zones":["South"],"states":["Tamil Nadu","Andhra Pradesh","Puducherry"],"cities":["Chennai","Visakhapatnam"],"description":"Cyclone Fengal — Tamil Nadu and Andhra Pradesh coastal disruption","impact_on_demand":"very_low","source":"IMD","tags":["cyclone","south_india","crisis"]},

    # ══════════════════════════════════════════════════════════════════
    # 2026 UPCOMING EVENTS — Jun to Dec 2026
    # ══════════════════════════════════════════════════════════════════

    # Government Holidays 2026
    {"id":"GH012","category":"Government Holiday","subcategory":"National Holiday","name":"Independence Day 2026","start_date":"2026-08-15","end_date":"2026-08-15","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"80th Independence Day 2026","impact_on_demand":"neutral_to_slight_up","source":"GoI","tags":["national","patriotic"]},
    {"id":"GH013","category":"Government Holiday","subcategory":"National Holiday","name":"Gandhi Jayanti 2026","start_date":"2026-10-02","end_date":"2026-10-02","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Gandhi Jayanti 2026","impact_on_demand":"neutral","source":"GoI","tags":["national"]},
    {"id":"GH014","category":"Government Holiday","subcategory":"National Holiday","name":"Dussehra / Govt Holiday 2026","start_date":"2026-10-01","end_date":"2026-10-01","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Dussehra Govt Holiday 2026","impact_on_demand":"slight_up","source":"GoI","tags":["national","dussehra"]},
    {"id":"GH015","category":"Government Holiday","subcategory":"National Holiday","name":"Diwali Govt Holiday 2026","start_date":"2026-11-08","end_date":"2026-11-09","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Diwali Govt Holiday 2026","impact_on_demand":"very_high_up","source":"GoI","tags":["national","diwali"]},
    {"id":"GH016","category":"Government Holiday","subcategory":"National Holiday","name":"Christmas 2026","start_date":"2026-12-25","end_date":"2026-12-25","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Christmas Day 2026","impact_on_demand":"slight_up","source":"GoI","tags":["national","christmas"]},

    # Festivals 2026
    {"id":"FE025","category":"Festival","subcategory":"Hindu","name":"Rath Yatra 2026","start_date":"2026-06-24","end_date":"2026-06-24","scope":"zone","zones":["East"],"states":["Odisha","West Bengal"],"cities":["Kolkata","Bhubaneswar"],"description":"Rath Yatra 2026 — high footfall in Puri/Kolkata","impact_on_demand":"high_up","source":"Hindu calendar","tags":["rath_yatra","odisha","east_india"]},
    {"id":"FE026","category":"Festival","subcategory":"Hindu","name":"Janmashtami 2026","start_date":"2026-08-16","end_date":"2026-08-16","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Janmashtami 2026 — celebrated pan India, midnight celebrations drive late orders","impact_on_demand":"slight_up","source":"Hindu calendar","tags":["janmashtami","krishna"]},
    {"id":"FE027","category":"Festival","subcategory":"Hindu","name":"Ganesh Chaturthi 2026","start_date":"2026-08-25","end_date":"2026-09-04","scope":"zone","zones":["West","South"],"states":["Maharashtra","Goa","Karnataka","Andhra Pradesh","Telangana"],"cities":["Mumbai","Navi Mumbai","Pune","Bengaluru","Hyderabad"],"description":"Ganesh Chaturthi 2026 — 11-day festival, very high Mumbai/Pune footfall","impact_on_demand":"high_up","source":"Hindu calendar","tags":["ganesh","maharashtra","festive"]},
    {"id":"FE028","category":"Festival","subcategory":"Hindu","name":"Onam 2026","start_date":"2026-09-04","end_date":"2026-09-04","scope":"zone","zones":["South"],"states":["Kerala"],"cities":["Kochi","Thiruvananthapuram"],"description":"Onam 2026 — Kerala harvest festival, highest footfall in Kerala","impact_on_demand":"very_high_up","source":"Malayalam calendar","tags":["onam","kerala","harvest"]},
    {"id":"FE029","category":"Festival","subcategory":"Hindu","name":"Navratri 2026","start_date":"2026-10-11","end_date":"2026-10-20","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Navratri 2026 — 9-night festival, high footfall in Gujarat, Delhi, Mumbai","impact_on_demand":"high_up","source":"Hindu calendar","tags":["navratri","garba","festive_season"]},
    {"id":"FE030","category":"Festival","subcategory":"Hindu","name":"Dussehra 2026","start_date":"2026-10-20","end_date":"2026-10-20","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Vijaya Dashami 2026","impact_on_demand":"slight_up","source":"Hindu calendar","tags":["dussehra"]},
    {"id":"FE031","category":"Festival","subcategory":"Hindu","name":"Durga Puja 2026","start_date":"2026-10-17","end_date":"2026-10-21","scope":"zone","zones":["East","North"],"states":["West Bengal","Bihar","Assam","Odisha","Delhi"],"cities":["Kolkata","New Delhi","Guwahati"],"description":"Durga Puja 2026 — peak festive event for East India","impact_on_demand":"very_high_up","source":"Bengali calendar","tags":["durga_puja","kolkata","bengal"]},
    {"id":"FE032","category":"Festival","subcategory":"Hindu","name":"Diwali 2026","start_date":"2026-11-08","end_date":"2026-11-11","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Diwali 2026 — peak consumer spending, high dining footfall","impact_on_demand":"very_high_up","source":"Hindu calendar","tags":["diwali","peak","festive_season"]},
    {"id":"FE033","category":"Festival","subcategory":"Regional","name":"Pongal 2026","start_date":"2026-01-14","end_date":"2026-01-17","scope":"zone","zones":["South"],"states":["Tamil Nadu","Andhra Pradesh","Telangana"],"cities":["Chennai","Hyderabad","Visakhapatnam"],"description":"Pongal 2026 — South Indian harvest festival","impact_on_demand":"high_up","source":"Tamil calendar","tags":["pongal","south_india","harvest"]},

    # Sports Events 2026
    {"id":"SP009","category":"Sports Event","subcategory":"Cricket","name":"ICC World Test Championship Final 2026","start_date":"2026-06-11","end_date":"2026-06-15","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"WTC Final 2026 — India potentially playing, drives evening delivery surge","impact_on_demand":"slight_up","source":"ICC","tags":["cricket","wtc","world_test"]},
    {"id":"SP010","category":"Sports Event","subcategory":"Cricket","name":"India vs England Test Series 2026","start_date":"2026-07-01","end_date":"2026-08-10","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"India tour of England 2026 — morning match timings drive breakfast/brunch orders","impact_on_demand":"slight_up","source":"BCCI/ECB","tags":["cricket","test","england"]},
    {"id":"SP011","category":"Sports Event","subcategory":"Cricket","name":"Asia Cup 2026","start_date":"2026-09-01","end_date":"2026-09-20","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Asia Cup 2026 — India matches drive strong delivery surge","impact_on_demand":"high_up","source":"ACC","tags":["cricket","asia_cup","tournament"]},

    # Commercial Events 2026
    {"id":"CE008","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Amazon Prime Day 2026","start_date":"2026-07-15","end_date":"2026-07-16","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Amazon Prime Day 2026 — drives footfall around deals and dining","impact_on_demand":"slight_up","source":"Amazon","tags":["amazon","prime_day","ecommerce"]},
    {"id":"CE009","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Flipkart Big Billion Days 2026","start_date":"2026-10-05","end_date":"2026-10-10","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Flipkart BBD 2026 — festive season sale","impact_on_demand":"slight_up","source":"Flipkart","tags":["flipkart","sale","ecommerce"]},
    {"id":"CE010","category":"Commercial Event","subcategory":"E-commerce Sale","name":"Amazon Great Indian Festival 2026","start_date":"2026-10-04","end_date":"2026-10-13","scope":"pan_india","zones":[],"states":[],"cities":[],"description":"Amazon festive season sale 2026","impact_on_demand":"slight_up","source":"Amazon","tags":["amazon","sale","ecommerce"]},

    # Emergency Crisis 2026
    {"id":"EC008","category":"Emergency Crisis","subcategory":"Heatwave","name":"North India Pre-Monsoon Heatwave 2026","start_date":"2026-06-01","end_date":"2026-06-20","scope":"zone","zones":["North","Central"],"states":["Delhi","Uttar Pradesh","Haryana","Rajasthan","Madhya Pradesh"],"cities":["New Delhi","Jaipur","Ludhiana","Lucknow"],"description":"IMD Red/Orange alert — temperatures 42-46°C across North India. Strong suppressor on outdoor footfall.","impact_on_demand":"low","source":"IMD","tags":["heatwave","north_india","extreme_heat","crisis"]},
    {"id":"EC009","category":"Emergency Crisis","subcategory":"Air Quality","name":"Winter Smog Emergency Delhi 2026","start_date":"2026-11-05","end_date":"2026-11-25","scope":"city","zones":["North"],"states":["Delhi","Haryana","Punjab"],"cities":["New Delhi","Ludhiana"],"description":"Annual winter AQI emergency — GRAP restrictions, school closures, WFH advisory","impact_on_demand":"low","source":"CPCB / Delhi Govt","tags":["aqi","smog","delhi","crisis"]},
]

def get_all_events():
    return EVENTS_DB


def _event_applies_to_geo(ev: dict, city: str = None,
                           state: str = None, zone: str = None) -> bool:
    from data.india_geo import CITIES
    """
    Returns True if an event applies to the requested geography.

    Rules:
      pan_india  → always applies to every city/state/zone
      zone       → applies only if the city's zone OR the requested zone is in ev["zones"]
      state      → applies only if the city's state OR the requested state is in ev["states"]
      city       → applies only if the city is in ev["cities"]

    When city is given, we resolve its zone and state from CITIES and use those
    to evaluate zone-scoped and state-scoped events correctly.
    """
    scope = ev.get("scope", "pan_india")

    if scope == "pan_india":
        return True

    # Resolve city → zone + state if city is provided
    city_zone  = CITIES.get(city, {}).get("zone")  if city  else None
    city_state = CITIES.get(city, {}).get("state") if city  else None

    if scope == "zone":
        ev_zones = ev.get("zones", [])
        if city:
            # The event must cover the zone this city belongs to
            return city_zone in ev_zones if city_zone else False
        if zone:
            return zone in ev_zones
        return True  # no geo filter requested → include all zone events

    if scope == "state":
        ev_states = ev.get("states", [])
        if city:
            return city_state in ev_states if city_state else False
        if state:
            return state in ev_states
        return True

    if scope == "city":
        ev_cities = ev.get("cities", [])
        if city:
            return city in ev_cities
        if state:
            # Include city-scoped event if any of its cities are in the requested state
            return any(CITIES.get(c, {}).get("state") == state for c in ev_cities)
        if zone:
            return any(CITIES.get(c, {}).get("zone") == zone for c in ev_cities)
        return True

    return True


def get_events_by_date(date_str: str, city: str = None,
                       state: str = None, zone: str = None):
    """Return all events active on date_str filtered by geography."""
    from datetime import date as dt_date
    d = dt_date.fromisoformat(date_str)
    results = []
    for ev in EVENTS_DB:
        start = dt_date.fromisoformat(ev["start_date"])
        end   = dt_date.fromisoformat(ev["end_date"])
        if not (start <= d <= end):
            continue
        if not _event_applies_to_geo(ev, city=city, state=state, zone=zone):
            continue
        results.append(ev)
    return results


def get_events_by_range(start_date: str, end_date: str,
                        category: str = None, city: str = None,
                        state: str = None, zone: str = None):
    """Return all events overlapping date range, filtered by category and geography."""
    from datetime import date as dt_date
    s = dt_date.fromisoformat(start_date)
    e = dt_date.fromisoformat(end_date)
    results = []
    for ev in EVENTS_DB:
        ev_start = dt_date.fromisoformat(ev["start_date"])
        ev_end   = dt_date.fromisoformat(ev["end_date"])
        if ev_end < s or ev_start > e:
            continue
        if category and ev["category"] != category:
            continue
        if not _event_applies_to_geo(ev, city=city, state=state, zone=zone):
            continue
        results.append(ev)
    return results
