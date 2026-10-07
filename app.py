import sqlite3
import pandas as pd

from flask import Flask, render_template, request

from recommend import recommend


app = Flask(__name__)


# --------------------------------------------------
# DATABASE OPTIONS
# --------------------------------------------------

def get_options():

    conn = sqlite3.connect("emergency_admit.db")

    localities = pd.read_sql(
        "SELECT locality_name FROM dim_locality",
        conn
    )["locality_name"].tolist()

    etypes = pd.read_sql(
        "SELECT emergency_type FROM dim_emergency_type",
        conn
    )["emergency_type"].tolist()

    conn.close()

    return localities, etypes


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    localities, etypes = get_options()

    if request.method == "POST":

        selected_locality = request.form.get("locality")
        selected_etype = request.form.get("etype")

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        try:

            result = recommend(
                selected_locality,
                selected_etype
            )

            if result is None or result.empty:

                return render_template(
                    "results.html",
                    results=[],
                    locality=selected_locality,
                    emergency_type=selected_etype,
                    error="No suitable hospital was found."
                )

            # Convert DataFrame into list of dictionaries
            results = result.to_dict(orient="records")

            return render_template(
                "results.html",
                results=results,
                locality=selected_locality,
                emergency_type=selected_etype,
                latitude=latitude,
                longitude=longitude,
                error=None
            )

        except Exception as e:

            return render_template(
                "results.html",
                results=[],
                locality=selected_locality,
                emergency_type=selected_etype,
                error=str(e)
            )

    return render_template(
        "index.html",
        localities=localities,
        etypes=etypes
    )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("emergency_admit.db")

    hospitals = pd.read_sql(
        "SELECT * FROM dim_hospital",
        conn
    )

    emergency_types = pd.read_sql(
        "SELECT * FROM dim_emergency_type",
        conn
    )

    localities = pd.read_sql(
        "SELECT * FROM dim_locality",
        conn
    )

    facts = pd.read_sql(
        "SELECT * FROM fact_emergency_admission",
        conn
    )

    conn.close()

    return render_template(
        "dashboard.html",
        hospital_count=len(hospitals),
        emergency_count=len(emergency_types),
        locality_count=len(localities),
        admission_count=len(facts)
    )


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )