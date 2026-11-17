import ydb

endpoint = "grpc://localhost:2136"
database = "/local"

def create_table_and_insert():
    driver_config = ydb.DriverConfig(
        endpoint, database, credentials=ydb.credentials.AnonymousCredentials()
    )
    with ydb.Driver(driver_config) as driver:
        driver.wait(timeout=5, fail_fast=True)

        with ydb.QuerySessionPool(driver) as pool:
            pool.execute_with_retries("""
                CREATE TABLE sensors (
                    sensor_id Uint64,
                    location Utf8,
                    last_seen Timestamp,
                    status Utf8,
                    PRIMARY KEY (sensor_id)
                )
            """)
            print("Таблица sensors создана.")

            pool.execute_with_retries("""
                INSERT INTO sensors (sensor_id, location, last_seen, status)
                VALUES (1, 'ул. Ленина, д. 1', CurrentUtcTimestamp(), 'active')
            """)
            print("Тестовая запись вставлена.")

            result = pool.execute_with_retries("SELECT * FROM sensors")
            for row in result[0].rows:
                print(f"Прочитано: {row}")

if __name__ == "__main__":
    create_table_and_insert()
