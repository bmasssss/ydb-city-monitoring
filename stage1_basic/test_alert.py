import ydb

endpoint = "grpc://localhost:2136"
database = "/local"

with ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.credentials.AnonymousCredentials()) as driver:
    driver.wait(timeout=5, fail_fast=True)
    with ydb.QuerySessionPool(driver) as pool:
        pool.execute_with_retries("""
            INSERT INTO sensor_readings (sensor_id, timestamp, temperature, humidity)
            VALUES (999, CurrentUtcTimestamp(), 35.5, 50.0)
        """)
        print("Тестовая запись с перегревом (35.5°C) вставлена!")
