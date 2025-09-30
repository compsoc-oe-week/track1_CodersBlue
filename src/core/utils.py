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

import re
from datetime import datetime, timedelta

def parse_size_filter(size_str):
    """
    Parses a size filter string (e.g., '>10MB', '<1.5KB') into an operator and size in bytes.
    """
    if not size_str:
        return None, None

    # Allow for floating point values
    match = re.match(r'([><=])\s*(\d+\.?\d*)\s*([KMGT]?B)', size_str, re.IGNORECASE)
    if not match:
        return None, None

    op, val, unit = match.groups()
    val = float(val)
    unit = unit.upper()

    if unit == 'KB':
        val *= 1024
    elif unit == 'MB':
        val *= 1024**2
    elif unit == 'GB':
        val *= 1024**3
    elif unit == 'TB':
        val *= 1024**4

    return op, int(val)

def parse_date_filter(date_str):
    """
    Parses a date filter string (e.g., '>7d', '<1m') into an operator and a datetime object.
    """
    if not date_str:
        return None, None

    match = re.match(r'([><=])\s*(\d+)\s*([dwmy])', date_str, re.IGNORECASE)
    if not match:
        return None, None

    op, val, unit = match.groups()
    val = int(val)
    unit = unit.lower()

    now = datetime.now()
    if unit == 'd':
        delta = timedelta(days=val)
    elif unit == 'w':
        delta = timedelta(weeks=val)
    elif unit == 'm':
        # Approximate months as 30 days
        delta = timedelta(days=val * 30)
    elif unit == 'y':
        # Approximate years as 365 days
        delta = timedelta(days=val * 365)
    else:
        return None, None

    return op, now - delta

FILE_TYPE_MAPPINGS = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
    "spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "video": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "logs": [".log"],
}