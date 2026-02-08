import json
import os

class ConfigLoader:
    _config = None

    @classmethod
    def get_config(cls):
        """Loads and returns the configuration dictionary (singleton pattern)."""
        if cls._config is None:
            cls._load_config()
        return cls._config

    @classmethod
    def _load_config(cls):
        """Internal method to load config from JSON file."""
        # Calculate path relative to this file
        # this file is in src/utils/
        # config.json is in project root (two levels up)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        config_path = os.path.join(project_root, 'config.json')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                cls._config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse config.json: {e}")
