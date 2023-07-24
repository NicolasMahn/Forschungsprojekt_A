import pandas as pd
import random
import os
from datetime import datetime, timedelta


def generate_data(quantity, path, file_name):
    data = []
    priorities = [0, 1, 2, 3]

    for _ in range(quantity):
        status = True
        total_processing_time = random.randint(2, 50)
        remaining_processing_time = total_processing_time
        priority = random.choice(priorities)

        unix_time_ms = int(datetime.now().timestamp() * 1000)
        due_date = unix_time_ms + random.randint(100000, 1000000)

        data_point = {
            'status': status,
            'remaining_processing_time': remaining_processing_time,
            'total_processing_time': total_processing_time,
            'priority': priority,
            'due_date': due_date
        }
        data.append(data_point)

    df = pd.DataFrame(data)
    file_path = path + file_name + ".csv"
    df.to_csv(file_path)
    print(df)