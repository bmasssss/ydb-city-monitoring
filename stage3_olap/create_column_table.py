import ydb

endpoint = "grpc://localhost:2136"
database = "/local"

with ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.credentials.AnonymousCredentials()) as driver:
    driver.wait(timeout=5, fail_fast=True)
    with ydb.QuerySessionPool(driver) as pool:
        pool.execute_with_retries("""
            CREATE TABLE sensor_readings_column (
                sensor_id Uint64 NOT NULL,
                timestamp Timestamp NOT NULL,
                temperature Double,
                humidity Double,
                PRIMARY KEY (sensor_id, timestamp)
            )
            PARTITION BY HASH(sensor_id)
            WITH (
                STORE = COLUMN
            )
        """)
        print("Колоночная таблица создана.")
