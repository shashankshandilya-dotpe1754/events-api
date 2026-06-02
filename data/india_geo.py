"""
India geography: zones, states, cities with coordinates.
Used across weather, events, and filtering endpoints.
"""

ZONES = {
    "North":     ["Delhi", "Uttar Pradesh", "Haryana", "Punjab", "Himachal Pradesh",
                  "Uttarakhand", "Jammu & Kashmir", "Rajasthan"],
    "South":     ["Karnataka", "Tamil Nadu", "Andhra Pradesh", "Telangana",
                  "Kerala", "Puducherry"],
    "East":      ["West Bengal", "Bihar", "Odisha", "Jharkhand",
                  "Assam", "Chhattisgarh"],
    "West":      ["Maharashtra", "Gujarat", "Goa"],
    "Central":   ["Madhya Pradesh"],
    "Northeast": ["Arunachal Pradesh", "Manipur", "Meghalaya", "Mizoram",
                  "Nagaland", "Sikkim", "Tripura"],
}

STATE_ZONE = {}
for zone, states in ZONES.items():
    for s in states:
        STATE_ZONE[s] = zone

CITIES = {
    # North
    "New Delhi":   {"state": "Delhi",           "zone": "North", "lat": 28.6139, "lon": 77.2090},
    "Jaipur":      {"state": "Rajasthan",        "zone": "North", "lat": 26.9124, "lon": 75.7873},
    "Ludhiana":    {"state": "Punjab",           "zone": "North", "lat": 30.9010, "lon": 75.8573},
    "Chandigarh":  {"state": "Punjab",           "zone": "North", "lat": 30.7333, "lon": 76.7794},
    "Lucknow":     {"state": "Uttar Pradesh",    "zone": "North", "lat": 26.8467, "lon": 80.9462},
    "Noida":       {"state": "Uttar Pradesh",    "zone": "North", "lat": 28.5355, "lon": 77.3910},
    "Agra":        {"state": "Uttar Pradesh",    "zone": "North", "lat": 27.1767, "lon": 78.0081},
    "Varanasi":    {"state": "Uttar Pradesh",    "zone": "North", "lat": 25.3176, "lon": 82.9739},
    "Dehradun":    {"state": "Uttarakhand",      "zone": "North", "lat": 30.3165, "lon": 78.0322},
    "Amritsar":    {"state": "Punjab",           "zone": "North", "lat": 31.6340, "lon": 74.8723},
    # South
    "Bengaluru":   {"state": "Karnataka",        "zone": "South", "lat": 12.9716, "lon": 77.5946},
    "Hyderabad":   {"state": "Telangana",        "zone": "South", "lat": 17.3850, "lon": 78.4867},
    "Chennai":     {"state": "Tamil Nadu",       "zone": "South", "lat": 13.0827, "lon": 80.2707},
    "Kochi":       {"state": "Kerala",           "zone": "South", "lat": 9.9312,  "lon": 76.2673},
    "Coimbatore":  {"state": "Tamil Nadu",       "zone": "South", "lat": 11.0168, "lon": 76.9558},
    "Mysuru":      {"state": "Karnataka",        "zone": "South", "lat": 12.2958, "lon": 76.6394},
    "Visakhapatnam":{"state":"Andhra Pradesh",   "zone": "South", "lat": 17.6868, "lon": 83.2185},
    "Thiruvananthapuram":{"state":"Kerala",      "zone": "South", "lat": 8.5241,  "lon": 76.9366},
    # West
    "Mumbai":      {"state": "Maharashtra",      "zone": "West",  "lat": 19.0760, "lon": 72.8777},
    "Navi Mumbai": {"state": "Maharashtra",      "zone": "West",  "lat": 19.0330, "lon": 73.0297},
    "Pune":        {"state": "Maharashtra",      "zone": "West",  "lat": 18.5204, "lon": 73.8567},
    "Nagpur":      {"state": "Maharashtra",      "zone": "West",  "lat": 21.1458, "lon": 79.0882},
    "Ahmedabad":   {"state": "Gujarat",          "zone": "West",  "lat": 23.0225, "lon": 72.5714},
    "Surat":       {"state": "Gujarat",          "zone": "West",  "lat": 21.1702, "lon": 72.8311},
    "Vadodara":    {"state": "Gujarat",          "zone": "West",  "lat": 22.3072, "lon": 73.1812},
    "Goa":         {"state": "Goa",              "zone": "West",  "lat": 15.2993, "lon": 74.1240},
    # East
    "Kolkata":     {"state": "West Bengal",      "zone": "East",  "lat": 22.5726, "lon": 88.3639},
    "Bhubaneswar": {"state": "Odisha",           "zone": "East",  "lat": 20.2961, "lon": 85.8245},
    "Patna":       {"state": "Bihar",            "zone": "East",  "lat": 25.5941, "lon": 85.1376},
    "Ranchi":      {"state": "Jharkhand",        "zone": "East",  "lat": 23.3441, "lon": 85.3096},
    "Guwahati":    {"state": "Assam",            "zone": "East",  "lat": 26.1445, "lon": 91.7362},
    # Central
    "Bhopal":      {"state": "Madhya Pradesh",   "zone": "Central","lat": 23.2599, "lon": 77.4126},
    "Indore":      {"state": "Madhya Pradesh",   "zone": "Central","lat": 22.7196, "lon": 75.8577},
    "Raipur":      {"state": "Chhattisgarh",     "zone": "East",   "lat": 21.2514, "lon": 81.6296},
}

CITY_LIST   = sorted(CITIES.keys())
STATE_LIST  = sorted({v["state"] for v in CITIES.values()})
ZONE_LIST   = sorted(ZONES.keys())
