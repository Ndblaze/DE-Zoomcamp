import requests

# Direct download URL
DIRECT_DOWNLOAD_URL = "https://www.kaggle.com/api/v1/datasets/download/cityofLA/los-angeles-traffic-collision-data"

# Local file name to save the downloaded file
ZIP_FILENAME = "la_collision_data.zip"

# Function to download the file using requests
def download_file(url, filename):
    """Download file from the given URL and save it locally."""
    print(f"Downloading from {url}...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Download complete. File saved as {filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

# Download the file
download_file(DIRECT_DOWNLOAD_URL, ZIP_FILENAME)
