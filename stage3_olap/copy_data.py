import ydb

endpoint = "grpc://localhost:2136"
database = "/local"

def copy_data():
    with ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.credentials.AnonymousCredentials()) as driver:
        driver.wait(timeout=5, fail_fast=True)
        with ydb.QuerySessionPool(driver) as pool:
            print("Начинаю перенос данных...")
            # Выполняем вставку из одной таблицы в другую
            pool.execute_with_retries("""
                INSERT INTO sensor_readings_column
                SELECT sensor_id, timestamp, temperature, humidity
                FROM sensor_readings
            """)
            print("Перенос данных успешно завершен!")

if __name__ == "__main__":
    copy_data()
