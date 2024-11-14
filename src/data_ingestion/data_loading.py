import pandas as pd
import json
from typing import Optional, Dict

class DataLoader:
    """
    A class for loading and caching board game data from various sources.
    """
    def __init__(self, config_path: str = "config.json"):
        """
        Initializes DataLoader with configuration from a JSON file.

        Parameters:
        config_path (str): Path to the JSON configuration file.
        """
        self.config = self._load_config(config_path)
        self._cache = {}  

    def _load_config(self, config_path: str) -> Dict[str, str]:
        """
        Loads the configuration from a JSON file.

        Parameters:
        config_path (str): Path to the JSON configuration file.

        Returns:
        Dict[str, str]: Configuration with paths to data files.
        """
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            print("Configuration loaded successfully.")
            return config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return {}

    def load_data(self, data_type: str) -> Optional[pd.DataFrame]:
        """
        Loads data of the specified type (e.g., "reviews_15m", "game_details").

        Parameters:
        data_type (str): Type of data to load ("reviews_15m", "reviews_19m", "game_details", "game_id_20", "game_id_22").

        Returns:
        Optional[pd.DataFrame]: Loaded data if it exists in the configuration.
        """
        if data_type in self._cache:
            print(f"Using cached data for '{data_type}'")
            return self._cache[data_type]

        file_path = self.config.get(data_type)
        if not file_path:
            print(f"File for '{data_type}' not specified in the configuration.")
            return None

        try:
            data = pd.read_csv(file_path, low_memory=False)
            self._cache[data_type] = data  # Store in cache
            print(f"File {file_path} loaded successfully for '{data_type}'. Number of records: {len(data)}")
            return data
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None

    def clear_cache(self):
        """
        Clears cached data.
        """
        self._cache.clear()
        print("Data cache cleared.")

"""
Testing data
"""
data_loader = DataLoader("config.json")


reviews_15m = data_loader.load_data("reviews_15m")
reviews_19m = data_loader.load_data("reviews_19m")
game_details = data_loader.load_data("game_details")
game_id_20 = data_loader.load_data("game_id_20")
game_id_22 = data_loader.load_data("game_id_22")


if reviews_15m is not None and reviews_19m is not None:
    all_reviews = pd.concat([reviews_15m, reviews_19m], ignore_index=True)
    print(f"Total number of reviews: {len(all_reviews)}")


if game_id_20 is not None and game_id_22 is not None:
    all_games = pd.concat([game_id_20, game_id_22], ignore_index=True)
    print(f"Total number of games in two years: {len(all_games)}")

data_loader.clear_cache()