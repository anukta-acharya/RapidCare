# 🚑 RapidCare – Emergency Hospital Recommendation System

RapidCare is an **Emergency Hospital Recommendation System** developed using **Data Mining and Data Warehousing** concepts.

The system recommends and ranks suitable hospitals based on the patient's **locality** and **emergency type**. The recommendation considers hospital resources, distance, ICU availability, available beds, waiting time, and specialist doctors.

The project is designed as an academic prototype for **Bhubaneswar and the wider Khordha region of Odisha**.

---

## 📌 Project Overview

During an emergency, selecting the nearest hospital does not always guarantee that the required medical facilities are available.

RapidCare addresses this problem by analyzing hospital and emergency-related data and ranking hospitals according to their suitability for a particular emergency.

The system uses:

- Data Warehousing
- ETL processing
- Star Schema
- SQL-based data storage
- Data Mining
- K-Means Clustering
- Pattern Analysis
- Decision Tree Classification
- Weighted Hospital Ranking
- Geographic Distance Calculation
- Flask Web Application

---

## 🎯 Objectives

The main objectives of RapidCare are:

1. Recommend suitable hospitals for emergency situations.
2. Rank hospitals according to multiple emergency-related factors.
3. Store hospital and emergency information using a data warehouse structure.
4. Apply data mining techniques to identify useful patterns.
5. Cluster hospitals according to their available resources.
6. Analyze emergency outcomes and hospital patterns.
7. Provide a simple web interface for users.
8. Demonstrate the practical application of Data Mining and Data Warehousing concepts.

---

## ✨ Key Features

### 🏥 Emergency Hospital Recommendation

Users can select:

- Patient locality
- Emergency type

RapidCare then generates a ranked list of suitable hospitals.

### 📍 Locality-Based Recommendation

The system contains locality information including:

- Locality name
- Zone
- Latitude
- Longitude
- Population density tier

The current dataset contains **50 localities**.

### 🚨 Emergency Type Selection

The system supports **8 emergency categories** with information such as:

- Emergency type
- Required specialty
- Required resources
- Severity level
- Golden-hour limit

### 🏨 Hospital Resource Analysis

Hospital ranking considers:

- Available beds
- ICU availability
- Ventilator availability
- Specialist doctors
- Average waiting time
- Hospital distance
- Trauma center availability
- Blood bank availability

### 📊 Hospital Ranking

Hospitals are ranked using a weighted scoring approach.

The current weights are:

| Factor | Weight |
|---|---:|
| Distance | 35% |
| ICU Availability | 20% |
| Bed Availability | 15% |
| Waiting Time | 15% |
| Specialist Doctors | 15% |

### 📈 Data Mining

The project includes:

- K-Means Clustering
- Pattern Analysis
- Decision Tree Classification

### 🗺️ Geographic Distance

The system uses the **Haversine formula** to calculate the geographical distance between the selected locality and hospitals.

### 🌐 Web Application

The backend is developed using **Flask** and the frontend uses:

- HTML
- CSS
- JavaScript
- Jinja templates

---

## 🏗️ System Architecture

The overall workflow of RapidCare is:

```text
                 ┌──────────────────────┐
                 │      User Input      │
                 │ Locality + Emergency │
                 │        Type          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Flask Backend     │
                 │       app.py        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Recommendation     │
                 │       Engine         │
                 │    recommend.py      │
                 └──────────┬───────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │       SQLite Database       │
              │      Data Warehouse         │
              └─────────────┬───────────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌──────────────┐
      │ Hospitals  │ │ Localities │ │ Emergency    │
      │ Dimension  │ │ Dimension  │ │ Type         │
      └────────────┘ └────────────┘ │ Dimension    │
                                    └──────────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Ranked Hospitals   │
                 │      Top 5 Results   │
                 └──────────────────────┘
