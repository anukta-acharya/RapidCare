"""
mining_analysis.py
The actual "data mining" part of the project. Run this after load_data.py.

1. Clustering: groups hospitals into capability tiers (KMeans)
2. Pattern analysis: most common emergency type per locality,
   average wait time by hospital type, outcome distribution by severity
3. Classification: predicts admission outcome from emergency + hospital features

Outputs:
- Printed tables in the terminal
- hospital_clusters.png, outcome_by_severity.png saved in this folder
"""

import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

DB_PATH = "emergency_admit.db"


def load_tables():
    conn = sqlite3.connect(DB_PATH)
    hospitals = pd.read_sql("SELECT * FROM dim_hospital", conn)
    facts = pd.read_sql("SELECT * FROM fact_emergency_admission", conn)
    etypes = pd.read_sql("SELECT * FROM dim_emergency_type", conn)
    conn.close()
    return hospitals, facts, etypes


# ---------- 1. CLUSTERING: group hospitals by capability ----------
def cluster_hospitals(hospitals, k=3):
    features = hospitals[["total_beds", "icu_beds", "ventilators", "specialist_doctors"]]
    scaled = StandardScaler().fit_transform(features)

    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    hospitals["capability_cluster"] = km.fit_predict(scaled)

    # Label clusters by average bed count (small / medium / large capability)
    cluster_means = hospitals.groupby("capability_cluster")["total_beds"].mean().sort_values()
    labels = {cid: name for cid, name in zip(cluster_means.index, ["Basic", "Mid-tier", "Major/Tertiary"])}
    hospitals["capability_tier"] = hospitals["capability_cluster"].map(labels)

    print("\n=== Hospital Capability Clusters ===")
    print(hospitals.groupby("capability_tier")["hospital_name"]
          .apply(lambda x: ", ".join(x)).to_string())

    # simple bar chart of cluster sizes
    plt.figure(figsize=(6, 4))
    hospitals["capability_tier"].value_counts().plot(kind="bar", color="#4a7c9b")
    plt.title("Number of Hospitals per Capability Tier")
    plt.ylabel("Number of hospitals")
    plt.tight_layout()
    plt.savefig("static/images/hospital_clusters.png")
    plt.close()
    print("Saved chart: hospital_clusters.png")

    return hospitals


# ---------- 2. PATTERN ANALYSIS ----------
def pattern_analysis(hospitals, facts, etypes):
    print("\n=== Most common emergency type per locality ===")
    top_type = (
        facts.groupby("patient_locality_name")["emergency_type"]
        .agg(lambda x: x.value_counts().idxmax())
    )
    print(top_type.to_string())

    print("\n=== Average hospital wait time by hospital type ===")
    merged = facts.merge(hospitals[["hospital_id", "hospital_type"]], on="hospital_id")
    print(merged.groupby("hospital_type")["hospital_wait_time_min"].mean().round(1).to_string())

    print("\n=== Outcome distribution by severity level ===")
    merged2 = facts.merge(etypes[["emergency_type_id", "severity_level"]], on="emergency_type_id")
    outcome_table = pd.crosstab(merged2["severity_level"], merged2["outcome"], normalize="index") * 100
    print(outcome_table.round(1).to_string())

    plt.figure(figsize=(7, 4))
    outcome_table.plot(kind="bar", stacked=True, ax=plt.gca(), colormap="tab20")
    plt.title("Outcome Distribution by Emergency Severity (%)")
    plt.ylabel("Percentage of cases")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig("static/images/outcome_by_severity.png")
    plt.close()
    print("Saved chart: outcome_by_severity.png")


# ---------- 3. CLASSIFICATION: predict outcome ----------
def classify_outcome(facts, hospitals, etypes):
    df = facts.merge(hospitals[["hospital_id", "hospital_type", "occupancy_percent"]], on="hospital_id")
    df = df.merge(etypes[["emergency_type_id", "severity_level"]], on="emergency_type_id")

    features = pd.get_dummies(
        df[["hospital_type", "severity_level", "ambulance_used", "distance_km",
            "travel_time_min", "hospital_wait_time_min", "occupancy_percent"]],
        columns=["hospital_type", "severity_level", "ambulance_used"]
    )
    target = df["outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.25, random_state=42, stratify=target
    )

    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)

    print("\n=== Decision Tree: Predicting Admission Outcome ===")
    print(classification_report(y_test, preds, zero_division=0))

    importance = pd.Series(clf.feature_importances_, index=features.columns).sort_values(ascending=False)
    print("Top features influencing outcome:")
    print(importance.head(5).round(3).to_string())


if __name__ == "__main__":
    hospitals, facts, etypes = load_tables()
    hospitals = cluster_hospitals(hospitals)
    pattern_analysis(hospitals, facts, etypes)
    classify_outcome(facts, hospitals, etypes)