import json
import pandas as pd

class DataLoader:
    """
    A class for loading and caching board game data from various sources.
    """
    def __init__(self, config_path: str = "config.json"):
        """
        Initializes DataLoader with the path to the configuration file.
        """
        self.config_path = config_path
        self.config = None
        self._cache = {}

    def load_config(self):
        """
        Loads the configuration.
        """
        if self.config is None:
            try:
                with open(self.config_path, "r") as f:
                    self.config = json.load(f)
                print("Configuration loaded successfully.")
            except Exception as e:
                print(f"Error loading configuration: {e}")
                self.config = {}

    def load_data(self, data_type: str):
        """
        Loads data of the specified type after ensuring the config is loaded.
        """
        self.load_config() 
        if data_type in self._cache:
            print(f"Using cached data for '{data_type}'")
            return self._cache[data_type]

        file_path = self.config.get(data_type)
        if not file_path:
            print(f"File for '{data_type}' not specified in the configuration.")
            return None

        try:
            data = pd.read_csv(file_path, low_memory=False)
            self._cache[data_type] = data
            print(f"File {file_path} loaded successfully for '{data_type}'. Number of records: {len(data)}")
            return data
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None
