from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
from google.cloud import storage
import requests
import zipfile
import os
import pandas as pd


# ============ CONFIG ================
BUCKET_NAME = "la-traffic-collision"
GCP_PROJECT = "taxi-rides-ny-450705"
BQ_DATASET = "la_traffic_collision"
BQ_TABLE = "traffic_collisions"
ZIP_FILENAME = "la_collision_data.zip"
CSV_FILENAME = "Traffic_Collision_Data.csv"
DIRECT_DOWNLOAD_URL = "https://www.kaggle.com/api/v1/datasets/download/cityofLA/los-angeles-traffic-collision-data"
# ====================================

# Set GCP credentials (for local development or Airflow environment)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nd_blaze/nd_blaze.dev/python_dev/DataEngineering/ZoomCamp/Assignments/Project/taxi-rides-ny-450705-22c7a8da4f6d.json"


# Initialize GCP client
storage_client = storage.Client()


def download_file(url, filename, ti):
    """Download ZIP file using requests."""
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(1024):  # Removed tqdm
                f.write(chunk)
        print(f"Downloaded to {filename}")
        ti.xcom_push(key="downloaded_file", value=filename)
    else:
        raise Exception(f"Download failed with status code: {response.status_code}")



def unzip_file(ti):
    """Unzip the downloaded file."""
    zip_file = ti.xcom_pull(key="downloaded_file", task_ids="download_la_collision_data")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall()
        extracted_files = zip_ref.namelist()
        print("Extracted:", extracted_files)
        # Check for the correct CSV filename
        expected_csv = "traffic-collision-data-from-2010-to-present.csv"
        if expected_csv in extracted_files:
            ti.xcom_push(key="unzipped_file", value=expected_csv)
        else:
            raise Exception(f"Expected CSV '{expected_csv}' not found in the ZIP.")


# def upload_to_gcs(bucket_name, ti):
#     """Upload CSV file to GCS."""
#     filename = ti.xcom_pull(key="unzipped_file", task_ids="unzip_file")
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(filename)
#     blob.upload_from_filename(filename)
#     print(f"Uploaded {filename} to gs://{bucket_name}/{filename}")

def upload_to_gcs(bucket_name, ti):
    """Clean CSV headers and upload file to GCS."""
    filename = ti.xcom_pull(key="unzipped_file", task_ids="unzip_file")

    # Step 1: Read CSV into DataFrame
    df = pd.read_csv(filename)

    # Step 2: Clean headers
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w]", "_", regex=True)
    )

    # Step 3: Overwrite the original CSV with cleaned headers
    df.to_csv(filename, index=False)

    # Step 4: Upload cleaned file to GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)

    print(f"Uploaded {filename} to gs://{bucket_name}/{filename}")

# Default DAG args
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 4, 5),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    "la_traffic_download_to_bq_via_url",
    default_args=default_args,
    description="Download LA traffic data from direct URL, upload to GCS, load into BigQuery",
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Tasks
download_task = PythonOperator(
    task_id="download_la_collision_data",
    python_callable=download_file,
    op_args=[DIRECT_DOWNLOAD_URL, ZIP_FILENAME],
    dag=dag,
)

unzip_task = PythonOperator(
    task_id="unzip_file",
    python_callable=unzip_file,
    dag=dag,
)

upload_task = PythonOperator(
    task_id="upload_to_gcs",
    python_callable=upload_to_gcs,
    op_args=[BUCKET_NAME],
    dag=dag,
)

gcs_to_bq_task = GCSToBigQueryOperator(
    task_id='load_csv_to_bigquery',
    bucket='la-traffic-collision',
    source_objects=['traffic-collision-data-from-2010-to-present.csv'],
    destination_project_dataset_table='la_traffic_collision.traffic_collisions',
    source_format='CSV',
    skip_leading_rows=1,
    write_disposition='WRITE_TRUNCATE',
    autodetect=True,
    field_delimiter=',',
    gcp_conn_id='google_cloud_default'
)

# Set task dependencies
download_task >> unzip_task >> upload_task >> gcs_to_bq_task
