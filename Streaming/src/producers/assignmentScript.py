
import json
import time
import os
import pandas as pd
from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)
t0 = time.time()

topic_name = 'green-trips'

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the absolute path to the CSV file
csv_file = os.path.join(script_dir, "green_tripdata_2019-10.csv")

# Read CSV File and Keep Only Required Columns
columns_to_keep = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount"
]

df = pd.read_csv(csv_file, usecols=columns_to_keep)
for _, row in df.iterrows():
    message = row.to_dict()  # Convert row to dictionary
    message["event_timestamp"] = time.time() * 1000  # Add timestamp

    producer.send(topic_name, value=message)
    print(f"Sent: {message}")
    time.sleep(0.05)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')