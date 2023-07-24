import pandas as pd
import os


def edd_sort(file_name: str, path: str, due_date_column: str):
    file_path = path + file_name + ".csv"
    df = pd.read_csv(file_path)
    sorted_df = df.sort_values(by=due_date_column)
    return sorted_df


def get_total_processing_time(sorted_df):
    return sorted_df["total_processing_time"].sum()


