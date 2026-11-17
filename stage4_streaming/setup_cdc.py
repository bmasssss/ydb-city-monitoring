import ydb

endpoint = "grpc://localhost:2136"
database = "/local"
topic_path = "/local/sensor_changes"
consumer_name = "alert_consumer"

with ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.credentials.AnonymousCredentials()) as driver:
    driver.wait(timeout=5, fail_fast=True)

    # 1. Создаем топик (очередь) и сразу создаем потребителя (consumer)
    try:
        driver.topic_client.create_topic(
            path=topic_path,
            consumers=[consumer_name]
        )
        print(f"Топик {topic_path} и потребитель {consumer_name} созданы.")
    except ydb.SchemeError:
        print(f"Топик {topic_path} уже существует. Пропускаем создание.")

    # 2. Включаем CDC для таблицы sensor_readings
    # Это заставит базу автоматически отправлять изменения в созданный топик
    with ydb.QuerySessionPool(driver) as pool:
        try:
            pool.execute_with_retries("""
                ALTER TABLE sensor_readings
                ADD CHANGEFEED sensor_feed WITH (FORMAT = 'JSON', MODE = 'UPDATES')
            """)
            print("CDC (sensor_feed) для таблицы sensor_readings успешно добавлен.")
        except ydb.SchemeError as e:
            # Если CDC уже был добавлен ранее, просто игнорируем ошибку
            print("CDC уже существует или произошла ошибка (возможно, уже добавлен).")
