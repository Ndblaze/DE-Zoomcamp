from google.cloud import storage
import requests
import gzip
import shutil
from tqdm import tqdm
from tenacity import retry, wait_fixed, stop_after_attempt

# Set your GCP bucket name
BUCKET_NAME = "analytical-engineer-assignment"

# Specify the month you want to download
months = [f"2019-{str(month).zfill(2)}" for month in range(1, 13)]  # List for all months in 2019

# Initialize GCP Storage Client
storage_client = storage.Client()

def download_file(url, filename):
    """Download file from GitHub."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in tqdm(response.iter_content(1024), desc=f"Downloading {filename}"):
                file.write(chunk)
        print(f"Downloaded {filename}")
        return True
    else:
        print(f"Failed to download {url}")
        return False

def unzip_file(gz_filename, csv_filename):
    """Unzip the .gz file and save it as .csv."""
    with gzip.open(gz_filename, 'rb') as f_in:
        with open(csv_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Unzipped {gz_filename} to {csv_filename}")

@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))  # Retry with a 2-second delay and stop after 5 attempts
def upload_to_gcs(bucket_name, source_file, destination_blob):
    """Upload a file to Google Cloud Storage with retries."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    print(f"Uploaded {source_file} to gs://{bucket_name}/{destination_blob}")

# Process each month for yellow_tripdata
for month in months:
    file_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{month}.csv.gz"
    gz_file = f"yellow_tripdata_{month}.csv.gz"
    csv_file = f"yellow_tripdata_{month}.csv"  # Unzipped file will be saved as .csv
    gcs_path = f"yellow_tripdata/{csv_file}"  # Organizing in a subfolder in GCS

    # Step 1: Download the file
    if download_file(file_url, gz_file):
        # Step 2: Unzip the file to .csv
        unzip_file(gz_file, csv_file)
        
        # Step 3: Upload the .csv to GCS
        upload_to_gcs(BUCKET_NAME, csv_file, gcs_path)

print("All files uploaded successfully!")
