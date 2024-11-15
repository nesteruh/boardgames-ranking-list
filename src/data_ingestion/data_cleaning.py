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
        os.makedirs(self.save_path, exist_ok=True)

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

# Initialize DataLoader and DataCleaner
data_loader = DataLoader("config.json")
data_cleaner = DataCleaner(save_path="project_data/processed/")

# Cleaning Script for Each Dataset

## 1. 2022-01-08.csv and 2020-08-19.csv
for dataset_name in ["game_id_20", "game_id_22"]:
    data = data_loader.load_data(dataset_name)
    if data is not None:
        
        # Remove redundant index column if it exists
        data = data_cleaner.remove_redundant_columns(data, columns_to_drop=["Unnamed: 0"])

        # Convert relevant columns to numeric
        data = data_cleaner.convert_to_numeric(data, columns=["Year", "Rank", "Users rated"])

        # Remove rows with low user ratings (e.g., below 30)
        data = data_cleaner.remove_low_rated_rows(data, column="Users rated", min_threshold=30)

        # Validate URLs
        data = data_cleaner.validate_urls(data, url_columns=["URL", "Thumbnail"])

        # Fill remaining missing values
        data = data_cleaner.fill_missing_values(data, fill_value=0)

        # Save cleaned dataset
        data_cleaner.save_data(data, f"cleaned_{dataset_name}.csv")

## 2. bgg-19m-reviews_forChatGPT.csv and bgg-15m-reviews_forChatGPT.csv
for dataset_name in ["reviews_15m", "reviews_19m"]:
    data = data_loader.load_data(dataset_name)
    if data is not None:
        
        # Attempt to clean rows with inconsistent field counts (assumes initial inspection)
        try:
            data = pd.read_csv(data_loader.config[dataset_name], error_bad_lines=False)
        except Exception as e:
            print(f"Failed to load '{dataset_name}': {e}")

        # Remove duplicates if any
        data = data_cleaner.remove_duplicates(data, subset=["user", "ID", "rating"])

        # Fill remaining missing values
        data = data_cleaner.fill_missing_values(data, fill_value=0)

        # Save cleaned dataset
        data_cleaner.save_data(data, f"cleaned_{dataset_name}.csv")

## 3. games_detailed_info.csv
game_details = data_loader.load_data("game_details")
if game_details is not None:
    
    # Drop columns with excessive NaN values, keeping important ones
    columns_to_drop = [
        "War Game Rank", "Children's Game Rank", "Accessory Rank",
        "Video Game Rank", "Amiga Rank", "Commodore 64 Rank"
    ]
    game_details = data_cleaner.remove_redundant_columns(game_details, columns_to_drop)

    # Normalize or drop nested/multi-value columns
    if "alternate" in game_details.columns:
        game_details = game_details.drop(columns=["alternate"])

    # Remove rows with minimal user engagement
    game_details = data_cleaner.remove_low_rated_rows(game_details, column="usersrated", min_threshold=50)

    # Fill remaining missing values
    game_details = data_cleaner.fill_missing_values(game_details, fill_value=0)

    # Remove duplicates
    game_details = data_cleaner.remove_duplicates(game_details, subset=["id"])

    # Save cleaned dataset
    data_cleaner.save_data(game_details, "cleaned_game_details.csv")
