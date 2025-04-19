
# 🚦 Los Angeles Traffic Collisions Data Pipeline Project

This project showcases a complete end-to-end data engineering pipeline built to ingest, transform, and visualize traffic collision data in Los Angeles. The project utilizes modern cloud and orchestration tools including **Google Cloud Platform**, **dbt**, **Airflow**, and **Docker** to deliver a scalable and maintainable analytics solution.


## 🧠 Overview

This project demonstrates a robust data pipeline designed for real-time analytics using modern tools and best practices in data engineering. From data ingestion to transformation and visualization, the system is fully automated, modular, and production-ready.

---

## 🧱 Tech Stack

- **Google Cloud Platform (GCP)**  
  - **BigQuery** for data warehousing  
  - **Cloud Storage** for raw data staging

- **dbt (Data Build Tool)**  
  - Used for data modeling, transformations, testing, and documentation  
  - Developed using the **dbt Web UI**

- **Apache Airflow**  
  - Orchestrates the entire ETL pipeline

- **Docker**  
  - Containerizes the development environment for reproducibility

---

## ⚙️ Pipeline Flow

1. **Ingestion**: Traffic collision data is pulled into Google Cloud Storage.
2. **Orchestration**: Airflow DAG triggers the dbt job.
3. **Transformation**: dbt runs staging, fact, and lookup models, applying:
   - Surrogate key generation
   - JSON flattening (e.g., geo fields)
   - Geospatial transformation (e.g., `POINT(long, lat)`)
   - Filtering and cleaning
4. **Testing & Validation**:
   - dbt's built-in tests (`unique`, `not_null`, `relationships`)
5. **Visualization**:
   - Final datasets are visualized using **Looker Studio** with geospatial support

---

## 📊 Key Features

- **Surrogate Key Creation** for consistent joins
- **Geospatial Parsing** using `ST_GEOGPOINT`
- **Relationship Testing** with dbt schema.yml
- **Normalized Lookup Tables** for area, premise, crime codes
- **Time Parsing & Validation** for `time_occurred`
- **Filtered Deduplication** using `row_number() over (...)`
---

## 📸 Demo

- Looker Studio dashboard showing:
  - Heatmaps of collisions
  - Trends over time
  - Drill-down by area and premise

---


## 🗺️ Project Architecture

![pipeline architecture](https://github.com/user-attachments/assets/a82a135d-6529-4cde-b932-333d5a00d8ac)


```

        +-------------+       +-------------+
        |   Kaggle    | <---> |   Python    |  
        +-------------+       +-------------+
                                     |
                                     v
                           +------------------+
                           |   Apache Airflow  |
                           +------------------+
                              |            |
                   +----------+            +----------+
                   v                                 v
         +---------------------+         +--------------------------+
         | Google Cloud Storage|         |     Google BigQuery      |
         +---------------------+         +--------------------------+
                                                      |
                                                      v
                                           +-----------------------+
                                           |         dbt           |
                                           | (data cleaning +      |
                                           | transformation)       |
                                           +-----------------------+
                                                      |
                                                      v
                                            +--------------------+
                                            |   Looker Studio    |
                                            | (dashboard & maps) |
                                            +--------------------+

```

---

## 🔧 Tools & Technologies

| Tool                | Purpose                            |
|---------------------|-------------------------------------|
| **Python**          | Data ingestion & preprocessing      |
| **Kaggle API**      | Source for real-world data          |
| **Apache Airflow**  | Workflow orchestration              |
| **Google Cloud Storage** | Raw data storage              |
| **Google BigQuery** | Cloud data warehouse                |
| **dbt**             | Data transformation & modeling      |
| **DLT**             | Declarative data ingestion          |
| **Looker Studio**   | Data visualization                  |
| **GitHub**          | Version control                     |

---


## 📊 Dashboard Features

The Looker Studio dashboard includes:
- 🚘 Collision hotspots using geospatial mapping
- 📍 Point data extracted from WKT (e.g., `POINT(-118.2371 34.0581)`) into `Latitude`, `Longitude`
- ⏰ Trends over time
- 🏙️ Breakdown by location, street, and severity

<img width="1512" alt="Dashboard" src="https://github.com/user-attachments/assets/959dff06-d621-441f-8c17-69ebb1557c2a" />

---

## 📁 Project Structure

```bash
.
├── dags/
│   └── airflow_dag.py               # DAG for end-to-end orchestration
├── dlt_pipeline/
│   ├── __init__.py
│   ├── source_config.py             # @dlt.source and @dlt.resource definitions
│   └── transformations.py           # Map/filter logic
├── dbt/
│   ├── models/
│   │   └── staging/
│   │       └── collision_data.sql   # Cleansed and modeled data
│   └── dbt_project.yml
├── looker_dashboard/
│   └── dashboard_screenshot.png     # Sample visual
├── raw_data/
│   └── la_traffic_collisions.csv    # Optional local backup
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

---

## ▶️ How to Run This Project

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/la-traffic-collisions-pipeline.git
cd la-traffic-collisions-pipeline
```

---

### 2. **Set Up Environment Variables**

Create a `.env` file or export the following variables:

```bash
export GOOGLE_PROJECT_ID=your-gcp-project-id
export GCS_BUCKET=your-bucket-name
export BIGQUERY_DATASET=your_dataset_name
export DBT_TARGET=your_target_profile
```

---

### 3. **Start the Project with Docker**

Spin up the containers (Airflow, dbt, etc.) using Docker Compose:

```bash
docker-compose up -d
```

> Make sure you have Docker and Docker Compose installed.

---

### 4. **Access Airflow UI**

Open Airflow in your browser:

```
http://localhost:8080
```

Use the default credentials:
- **Username:** `airflow`
- **Password:** `airflow`

Trigger the DAG: `la_traffic_pipeline`

---

### 5. **Run dbt Models via Web UI**

Once the DAG triggers the `dbt` job:
- Open the **dbt Web UI** (if exposed locally)
- Or view logs in Airflow to verify model execution

Alternatively, from within the container:

```bash
docker exec -it your_dbt_container_name bash
dbt run
```

To test the models:

```bash
dbt test
```

---

### 6. **View Transformed Data in BigQuery**

Once the pipeline runs, navigate to your BigQuery dataset in the GCP Console to explore:
- `fact_collision`
- `area_lookup`, `premise_lookup`, `crime_lookup`
- `stg_la_collision` (staging layer)

---

### 7. **Connect to Looker Studio **

You can connect your **Looker Studio dashboard** directly to BigQuery to visualize:
- Geospatial collision data
- Time trends
- Breakdown by area, premise, etc.

---

## 🙌 Acknowledgements

- Data Source: [Kaggle - Los Angeles Traffic Collision Dataset](https://www.kaggle.com/)
- Inspiration: This was built as a final project for the Data Engineering Zoomcamp, demonstrating practical application of the tools taught throughout the course.


