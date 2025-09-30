import logging
import os
import json

def setup_logging():
    """Sets up basic logging."""
    # TODO: Add more sophisticated logging (e.g., file-based, rotating logs)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging initialized.")

def load_config(config_path: str = "config.json"):
    """
    Loads a JSON configuration file.

    TODO: Add more robust config handling (e.g., environment variables, default values).
    """
    if not os.path.exists(config_path):
        logging.warning(f"Config file not found at {config_path}. Using default settings.")
        return {}
    with open(config_path, 'r') as f:
        return json.load(f)

def get_project_root() -> str:
    """
    Returns the absolute path to the project root.

    TODO: This might need to be more robust depending on the execution context.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))