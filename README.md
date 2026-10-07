# Emergency Admit

A Data Mining & Data Warehousing course project that recommends the
best-fit hospital in Bhubaneswar, Odisha for a sudden medical emergency,
based on locality, required resources, and simulated hospital availability.

## Folder structure

```
emergency_admit/
├── data/
│   ├── hospitals_bbsr.csv          # dim_hospital source data (37 hospitals)
│   ├── dim_locality.csv            # 15 Bhubaneswar localities
│   ├── dim_emergency_type.csv      # 8 emergency categories + required resources
│   ├── hospital_coords.csv         # lat/long lookup for each hospital
│   └── fact_emergency_admission.csv # 800 synthetic emergency records
├── schema.sql                      # star schema (SQLite)
├── load_data.py                    # builds emergency_admit.db from the CSVs
├── recommend.py                    # scoring/ranking engine (run standalone or import)
├── mining_analysis.py              # clustering, pattern mining, classification
├── app.py                          # tiny Flask web demo
├── requirements.txt
└── README.md
```

## Setup

1. Install Python 3.9+ if you don't already have it.
2. Open a terminal in this folder and install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run order

1. **Build the database** (do this first, and again any time a CSV changes):
   ```
   python3 load_data.py
   ```
   This creates `emergency_admit.db` in this folder.

2. **Try the recommendation engine** from the command line:
   ```
   python3 recommend.py
   ```
   It will show you the list of valid locality names and emergency types,
   then ask you to type one of each, and print a ranked hospital list.

3. **Run the data mining analysis**:
   ```
   python3 mining_analysis.py
   ```
   This prints:
   - Hospital capability clusters (KMeans)
   - Most common emergency type per locality
   - Average wait time by hospital type
   - Outcome distribution by severity
   - A decision tree predicting admission outcome, with feature importances

   It also saves two chart images in this folder:
   `hospital_clusters.png` and `outcome_by_severity.png`.

4. **Run the web demo** (optional, good for presenting):
   ```
   python3 app.py
   ```
   Then open `http://127.0.0.1:5000` in your browser. Pick a locality and
   emergency type from the dropdowns and see the ranked hospital table.

## Notes for your report

- All hospital resource figures (beds, ICU, ventilators, doctors) are
  **simulated but realistic** — live, real-time hospital availability data
  is not publicly available in India, so this is a standard and expected
  limitation to state clearly in your report.
- The scoring formula in `recommend.py` (`W_DISTANCE`, `W_ICU_AVAILABLE`,
  etc.) is intentionally simple and adjustable — explain your chosen
  weights in the report, and feel free to tune them.
- The `fact_emergency_admission.csv` records were generated using distance
  calculations (haversine formula) and severity-aware probability
  distributions, not pure random numbers — this is your "ETL/data
  generation methodology" section.
