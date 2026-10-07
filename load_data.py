"""
load_data.py
Creates the SQLite database 'emergency_admit.db' and loads all
the CSV files from data/ into it, following schema.sql.

Run this FIRST, before recommend.py or mining_analysis.py.
"""

import sqlite3
import pandas as pd

DB_PATH = "emergency_admit.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create tables from schema.sql
    with open("schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    print("Schema created.")

    # 2. Load dim_locality
    dim_locality = pd.read_csv("data/dim_locality.csv")

# Match CSV column name with database schema
    if "density_level" in dim_locality.columns:
        dim_locality = dim_locality.rename(
             columns={"density_level": "population_density_tier"}
    )

    dim_locality.to_sql(
         "dim_locality",
           conn,
           if_exists="append",
           index=False
     )

    print(f"Loaded {len(dim_locality)} rows into dim_locality")

    # 3. Load dim_emergency_type
    dim_etype = pd.read_csv("data/dim_emergency_type.csv")
    dim_etype.to_sql("dim_emergency_type", conn, if_exists="append", index=False)
    print(f"Loaded {len(dim_etype)} rows into dim_emergency_type")

    # 4. Load dim_hospital, merged with coordinates
    hospitals = pd.read_csv("data/hospitals_bbsr.csv")
    coords = pd.read_csv("data/hospital_coords.csv")[["hospital_id", "latitude", "longitude"]]
    hospitals = hospitals.merge(coords, on="hospital_id", how="left")

    # convert Yes/No available_beds etc. already numeric; icu_available/ventilators_available numeric
    hospitals.to_sql("dim_hospital", conn, if_exists="append", index=False)
    print(f"Loaded {len(hospitals)} rows into dim_hospital")

    # 5. Load fact_emergency_admission
    facts = pd.read_csv("data/fact_emergency_admission.csv")
    facts.to_sql("fact_emergency_admission", conn, if_exists="append", index=False)
    print(f"Loaded {len(facts)} rows into fact_emergency_admission")

    conn.commit()
    conn.close()
    print("\nDone. Database saved as", DB_PATH)


if __name__ == "__main__":
    main()