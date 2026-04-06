import json
import os

class FileHandler:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.files = {
            "cars": os.path.join(self.data_dir, "cars.json"),
            "customers": os.path.join(self.data_dir, "customers.json"),
            "suppliers": os.path.join(self.data_dir, "suppliers.json"),
            "transactions": os.path.join(self.data_dir, "transactions.json")
        }
        self.initialize_files()

    def initialize_files(self):
        """Creates the required JSON files with empty dictionaries if they don't exist."""
        for name, path in self.files.items():
            if not os.path.exists(path):
                with open(path, "w") as f:
                    json.dump({}, f)  # Dict mapping IDs to attributes

    def load_data(self, entity_name):
        """Loads data dictionary from a specific JSON file."""
        if entity_name not in self.files:
            raise ValueError(f"Entity {entity_name} not supported.")
        path = self.files[entity_name]
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        except FileNotFoundError:
            self.initialize_files()
            return {}

    def save_data(self, entity_name, data):
        """Saves a dictionary back to the specific JSON file."""
        if entity_name not in self.files:
            raise ValueError(f"Entity {entity_name} not supported.")
        path = self.files[entity_name]
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
