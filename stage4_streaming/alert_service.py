import ydb
import json
import time

endpoint = "grpc://localhost:2136"
database = "/local"
topic_path = "/local/sensor_changes"
consumer_name = "alert_consumer"

def process_messages():
    print("Запуск сервиса алертов. Ожидание сообщений из топика...")

    with ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.credentials.AnonymousCredentials()) as driver:
        driver.wait(timeout=5, fail_fast=True)

        # Создаем читателя (reader) для топика
        reader = driver.topic_client.reader(topic_path, consumer=consumer_name)

        while True:
            try:
                # Ждем сообщение до 5 секунд
                message = reader.receive_message(timeout=5)

                if message:
                    print("\n!!! ПОЛУЧЕНО СООБЩЕНИЕ ИЗ ТОПИКА !!!")
                    # Декодируем JSON, который прислал CDC
                    data = json.loads(message.data.decode('utf-8'))
                    print(f"[DEBUG] Структура сообщения: {data}")

                    # В режиме UPDATES новые данные лежат в поле 'update'
                    record = data.get('update') or data.get('newImage') or data.get('new')

                    if record and 'temperature' in record:
                        temp = record['temperature']
                        # ID датчика (первичный ключ) приходит в массиве 'key'
                        sensor_id = data.get('key', ['unknown'])[0]

                        print(f"[INFO] Датчик {sensor_id}: Температура = {temp}°C")

                        if temp > 30.0:
                            print(f"🚨 [ALERT] ВНИМАНИЕ! Датчик {sensor_id} зафиксировал перегрев: {temp}°C!")
                        else:
                            print("[OK] Температура в норме.")
                    else:
                        print("[WARN] В сообщении не найдено поле 'temperature'.")

                    # Подтверждаем, что сообщение прочитано
                    reader.commit(message)

            except TimeoutError:
                # Это нормальная ситуация, когда новых сообщений нет.
                # Просто продолжаем цикл и ждем дальше.
                pass
            except Exception as e:
                # Если произошла реальная ошибка (например, сетевая), выводим её
                print(f"Ошибка при чтении: {type(e).__name__}: {e}")
                time.sleep(1)

if __name__ == "__main__":
    process_messages()
