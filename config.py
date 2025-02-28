# config.py
import json
import os

DEFAULT_CONFIG = {
    "model": "claude-3-7-sonnet-latest",
    "max_tokens": 1000,
    "default_approved_tools": []
}

def load_config(config_path="config.json"):
    """
    Load configuration from a JSON file or return default values if the file doesn't exist or is invalid.
    """
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {config_path}. Using default config.")
    return DEFAULT_CONFIG