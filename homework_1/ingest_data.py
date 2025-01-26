

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine




def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

        

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    if 'lpep_pickup_datetime' in df.columns:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')



    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)
            
    
            if 'lpep_pickup_datetime' in df.columns:
                df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
                df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)




# URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"

# python ingest_data.py \
#   --user=postgres \
#   --password=postgres \
#   --host=localhost \
#   --port=5433 \
#   --db=ny_taxi \
#   --table_name=green_taxi_trips \
#   --url=${URL}


# URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

# python ingest_data.py \
#   --user=postgres \
#   --password=postgres \
#   --host=localhost \
#   --port=5433 \
#   --db=ny_taxi \
#   --table_name=green_taxi_zones \
#   --url=${URL}



# sql codes:

# question 1

# SELECT count(trip_distance) 
# FROM green_taxi_trips
# WHERE lpep_pickup_datetime >= '2019-10-01' 
#   AND lpep_pickup_datetime < '2019-11-01'
#   AND lpep_dropoff_datetime >= '2019-10-01' 
#   AND lpep_dropoff_datetime < '2019-11-01'
#   AND trip_distance <= 1;


# SELECT count(trip_distance) 
# FROM green_taxi_trips
# WHERE lpep_pickup_datetime >= '2019-10-01' 
#   AND lpep_pickup_datetime < '2019-11-01'
#   AND lpep_dropoff_datetime >= '2019-10-01' 
#   AND lpep_dropoff_datetime < '2019-11-01'
#   AND trip_distance > 1 AND trip_distance <= 3;


# SELECT count(trip_distance) 
# FROM green_taxi_trips
# WHERE lpep_pickup_datetime >= '2019-10-01' 
#   AND lpep_pickup_datetime < '2019-11-01'
#   AND lpep_dropoff_datetime >= '2019-10-01' 
#   AND lpep_dropoff_datetime < '2019-11-01'
#   AND trip_distance > 3 AND trip_distance <= 7;


# SELECT count(trip_distance) 
# FROM green_taxi_trips
# WHERE lpep_pickup_datetime >= '2019-10-01' 
#   AND lpep_pickup_datetime < '2019-11-01'
#   AND lpep_dropoff_datetime >= '2019-10-01' 
#   AND lpep_dropoff_datetime < '2019-11-01'
#   AND trip_distance > 7 AND trip_distance <= 10;


# SELECT count(trip_distance) 
# FROM green_taxi_trips
# WHERE lpep_pickup_datetime >= '2019-10-01' 
#   AND lpep_pickup_datetime < '2019-11-01'
#   AND lpep_dropoff_datetime >= '2019-10-01' 
#   AND lpep_dropoff_datetime < '2019-11-01'
#   AND trip_distance > 10



# question 2

# SELECT lpep_pickup_datetime
# FROM green_taxi_trips
# where trip_distance = (select max(trip_distance) from green_taxi_trips)



# question 3

# SELECT * FROM
# (
# SELECT sum(total_amount) as total, "PULocationID"
# FROM green_taxi_trips 
# WHERE lpep_pickup_datetime >= '2019-10-18'
# AND  lpep_pickup_datetime < '2019-10-19'
# GROUP BY "PULocationID"
# ) as t
# LEFT JOIN green_taxi_zones z
# ON t."PULocationID" = z."LocationID"
# where t.total >13000


# questoin 4

# SELECT z."Zone"
# FROM green_taxi_trips t LEFT JOIN green_taxi_zones z
# ON t."DOLocationID" = z."LocationID"
# WHERE t."PULocationID" = 74 -- code for East Harlem North
#   AND lpep_pickup_datetime >= '2019-10-01'
#   AND lpep_pickup_datetime <= '2019-10-31'
#   AND t.tip_amount = (
#     SELECT MAX(t2.tip_amount)
#     FROM green_taxi_trips t2
#     WHERE t2."PULocationID" = 74
#       AND t2.lpep_pickup_datetime >= '2019-10-01'
#       AND t2.lpep_pickup_datetime <= '2019-10-31'
#   );
