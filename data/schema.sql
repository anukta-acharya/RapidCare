-- RapidCare: Data Warehouse Schema (Star Schema)
-- Fact table: fact_emergency_admission
-- Dimension tables: dim_hospital, dim_locality, dim_emergency_type

DROP TABLE IF EXISTS fact_emergency_admission;
DROP TABLE IF EXISTS dim_hospital;
DROP TABLE IF EXISTS dim_locality;
DROP TABLE IF EXISTS dim_emergency_type;

CREATE TABLE dim_hospital (
    hospital_id TEXT PRIMARY KEY,
    hospital_name TEXT,
    locality TEXT,
    ownership TEXT,
    hospital_type TEXT,
    total_beds INTEGER,
    available_beds INTEGER,
    icu_beds INTEGER,
    icu_available INTEGER,
    ventilators INTEGER,
    ventilators_available INTEGER,
    doctors_on_duty INTEGER,
    specialist_doctors INTEGER,
    ambulances_available INTEGER,
    blood_bank TEXT,
    trauma_center TEXT,
    occupancy_percent INTEGER,
    avg_wait_time_min INTEGER,
    latitude REAL,
    longitude REAL
);

CREATE TABLE dim_locality (
    locality_id TEXT PRIMARY KEY,
    locality_name TEXT,
    zone TEXT,
    latitude REAL,
    longitude REAL,
    density_level TEXT
);

CREATE TABLE dim_emergency_type (
    emergency_type_id TEXT PRIMARY KEY,
    emergency_type TEXT,
    required_specialty TEXT,
    required_resources TEXT,
    severity_level TEXT,
    golden_hour_minutes INTEGER
);

CREATE TABLE fact_emergency_admission (
    emergency_id TEXT PRIMARY KEY,
    patient_locality_id TEXT,
    patient_locality_name TEXT,
    emergency_type_id TEXT,
    emergency_type TEXT,
    hospital_id TEXT,
    hospital_name TEXT,
    admission_datetime TEXT,
    distance_km REAL,
    travel_time_min REAL,
    hospital_wait_time_min REAL,
    bed_type_assigned TEXT,
    required_specialty TEXT,
    ambulance_used TEXT,
    outcome TEXT,
    admission_status TEXT,
    FOREIGN KEY (patient_locality_id) REFERENCES dim_locality(locality_id),
    FOREIGN KEY (emergency_type_id) REFERENCES dim_emergency_type(emergency_type_id),
    FOREIGN KEY (hospital_id) REFERENCES dim_hospital(hospital_id)
);
