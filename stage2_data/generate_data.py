import csv
import random
from datetime import datetime, timedelta

NUM_RECORDS = 1_000_000
START_TIME = datetime(2025, 1, 1, 0, 0, 0)

def generate():
    with open('sensor_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sensor_id', 'timestamp', 'temperature', 'humidity'])

        for i in range(NUM_RECORDS):
            sensor_id = random.randint(1, 1000)
            ts = START_TIME + timedelta(seconds=i)
            temp = round(random.uniform(-10, 35), 2)
            hum = round(random.uniform(20, 100), 2)
            writer.writerow([sensor_id, ts.strftime('%Y-%m-%d %H:%M:%S'), temp, hum])

            if (i + 1) % 200000 == 0:
                print(f"Сгенерировано {i + 1} записей...")

if __name__ == "__main__":
    generate()
