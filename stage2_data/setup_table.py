import ydb

endpoint = "grpc://localhost:2136"
database = "/local"

with ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.credentials.AnonymousCredentials()) as driver:
    driver.wait(timeout=5, fail_fast=True)
    with ydb.QuerySessionPool(driver) as pool:
        pool.execute_with_retries("""
            CREATE TABLE sensor_readings (
                sensor_id Uint64,
                timestamp Timestamp,
                temperature Double,
                humidity Double,
                PRIMARY KEY (sensor_id, timestamp)
            )
        """)
        print("Таблица sensor_readings успешно создана.")
