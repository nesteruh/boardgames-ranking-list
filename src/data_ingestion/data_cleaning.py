import pandas as pd
import os
import sys
sys.path.append('src/data_ingestion/')
from data_loading import DataLoader

class DataCleaner:
    """
    A class for cleaning and preprocessing datasets.
    """

    def __init__(self, save_path: str = "data/processed/"):
        self.save_path = save_path

    def ensure_save_path(self):
        """
        Ensures the save path directory exists.
        """
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def remove_duplicates(self, data: pd.DataFrame, subset: list = None):
        """
        Removes duplicate rows from the dataset.
        
        Parameters:
        data (pd.DataFrame): The DataFrame to clean.
        subset (list): Columns to check for duplicates. If None, all columns are considered.
        Returns:
        pd.DataFrame: The DataFrame without duplicates.
        """
        return data.drop_duplicates(subset=subset)
    
    def remove_redundant_columns(self, data: pd.DataFrame, columns_to_drop: list):
        """Removes specified columns from the DataFrame."""
        data = data.drop(columns=columns_to_drop, errors="ignore")
        return data

    def convert_to_numeric(self, data: pd.DataFrame, columns: list):
        """Converts specified columns to numeric types, handling errors."""
        for col in columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        return data

    def remove_low_rated_rows(self, data: pd.DataFrame, column: str, min_threshold: int):
        """Removes rows where the specified column has values below a threshold."""
        initial_count = len(data)
        data = data[data[column] >= min_threshold]
        return data


    def fill_missing_values(self, data: pd.DataFrame, fill_value=0):
        """Fills all missing values with a specified fill value."""
        return data.fillna(fill_value)

    def validate_urls(self, data: pd.DataFrame, url_columns: list):
        """Checks for consistency in URL columns, removing rows with invalid URLs."""
        for col in url_columns:
            data[col] = data[col].apply(lambda x: x if isinstance(x, str) and x.startswith("http") else None)
        return data

    def save_data(self, data: pd.DataFrame, filename: str):
        """Saves the cleaned DataFrame to the specified directory."""
        file_path = os.path.join(self.save_path, filename)
        data.to_csv(file_path, index=False)
