"""
recommend.py
Core "best fit hospital" recommendation engine.

Run: python3 recommend.py
It will show you a list of localities and emergency types, then
ask you to pick one of each, and print a ranked list of hospitals.

Run load_data.py first to create emergency_admit.db.
"""

import sqlite3
import math
import pandas as pd

DB_PATH = "emergency_admit.db"

# Weights for the scoring formula -- tweak these and explain your
# reasoning in your project report.
W_DISTANCE = 0.35
W_ICU_AVAILABLE = 0.20
W_BED_AVAILABLE = 0.15
W_WAIT_TIME = 0.15
W_SPECIALISTS = 0.15


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def hospital_is_capable(row, required_resources):
    """Check whether a hospital has the resources an emergency type needs."""
    reqs = required_resources.split(";")
    for r in reqs:
        if r == "ICU" and row["icu_beds"] < 1:
            return False
        if r == "Ventilator" and row["ventilators"] < 1:
            return False
        if r == "Trauma Center" and row["trauma_center"] != "Yes":
            return False
        if r == "Blood Bank" and row["blood_bank"] != "Yes":
            return False
    return True


def normalize(series, invert=False):
    """Scale a pandas Series to 0-1. If invert=True, lower raw value = higher score."""
    if series.max() == series.min():
        return series.apply(lambda x: 1.0)
    scaled = (series - series.min()) / (series.max() - series.min())
    return 1 - scaled if invert else scaled


def recommend(locality_name, emergency_type_name, top_n=5):
    conn = sqlite3.connect(DB_PATH)

    locality = pd.read_sql(
        "SELECT * FROM dim_locality WHERE locality_name = ?", conn, params=(locality_name,)
    )
    if locality.empty:
        print("Locality not found. Check spelling / run list_options().")
        return None
    loc = locality.iloc[0]

    etype = pd.read_sql(
        "SELECT * FROM dim_emergency_type WHERE emergency_type = ?", conn, params=(emergency_type_name,)
    )
    if etype.empty:
        print("Emergency type not found. Check spelling / run list_options().")
        return None
    et = etype.iloc[0]

    hospitals = pd.read_sql("SELECT * FROM dim_hospital", conn)
    conn.close()

    # 1. Filter to capable hospitals
    capable = hospitals[hospitals.apply(lambda r: hospital_is_capable(r, et["required_resources"]), axis=1)].copy()
    if capable.empty:
        print("No hospital currently matches the required resources.")
        return None

    # 2. Distance
    capable["distance_km"] = capable.apply(
        lambda r: round(haversine(loc["latitude"], loc["longitude"], r["latitude"], r["longitude"]), 2), axis=1
    )

    # 3. Build normalized sub-scores (all 0-1, higher = better)
    capable["score_distance"] = normalize(capable["distance_km"], invert=True)
    capable["score_icu"] = normalize(capable["icu_available"])
    capable["bed_ratio"] = capable["available_beds"] / capable["total_beds"]
    capable["score_beds"] = normalize(capable["bed_ratio"])
    capable["score_wait"] = normalize(capable["avg_wait_time_min"], invert=True)
    capable["score_specialists"] = normalize(capable["specialist_doctors"])

    capable["final_score"] = (
        W_DISTANCE * capable["score_distance"]
        + W_ICU_AVAILABLE * capable["score_icu"]
        + W_BED_AVAILABLE * capable["score_beds"]
        + W_WAIT_TIME * capable["score_wait"]
        + W_SPECIALISTS * capable["score_specialists"]
    )

    ranked = capable.sort_values("final_score", ascending=False).head(top_n)

    print(f"\nBest-fit hospitals for '{emergency_type_name}' near '{locality_name}':\n")
    display_cols = [
        "hospital_name", "distance_km", "available_beds", "icu_available",
        "ventilators_available", "avg_wait_time_min", "final_score"
    ]
    print(ranked[display_cols].round(3).to_string(index=False))
    return ranked


def list_options():
    conn = sqlite3.connect(DB_PATH)
    localities = pd.read_sql("SELECT locality_name FROM dim_locality", conn)
    etypes = pd.read_sql("SELECT emergency_type FROM dim_emergency_type", conn)
    conn.close()
    print("Localities:\n", ", ".join(localities["locality_name"]))
    print("\nEmergency types:\n", ", ".join(etypes["emergency_type"]))


if __name__ == "__main__":
    list_options()
    loc_input = input("\nEnter locality name exactly as shown above: ").strip()
    et_input = input("Enter emergency type exactly as shown above: ").strip()
    recommend(loc_input, et_input)