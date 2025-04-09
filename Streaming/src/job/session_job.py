from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment
from pyflink.common.time import Duration

def create_trips_aggregated_sink(t_env):
    table_name = 'processed_taxi_sessions'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INT,
            DOLocationID INT,
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            trip_count BIGINT,
            PRIMARY KEY (PULocationID, DOLocationID, session_start) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name

def create_trips_source_kafka(t_env):
    table_name = "trips"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime TIMESTAMP(3),
            lpep_dropoff_datetime TIMESTAMP(3),
            PULocationID INT,
            DOLocationID INT,
            passenger_count INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            WATERMARK FOR lpep_dropoff_datetime AS lpep_dropoff_datetime - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def session_aggregation():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(3)

    # Set up the table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        # Create Kafka source table
        source_table = create_trips_source_kafka(t_env)
        
        # Create PostgreSQL sink table
        aggregated_table = create_trips_aggregated_sink(t_env)

        # Perform session window aggregation
        t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
        SELECT
            PULocationID,
            DOLocationID,
            window_start AS session_start,
            window_end AS session_end,
            COUNT(*) AS trip_count
        FROM TABLE(
            SESSION(TABLE {source_table}, DESCRIPTOR(lpep_dropoff_datetime), INTERVAL '5' MINUTES)
        )
        GROUP BY window_start, window_end, PULocationID, DOLocationID;
        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))

if __name__ == '__main__':
    session_aggregation()
