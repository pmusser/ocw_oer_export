"""
Module for extracting and loading data to/from JSON file
"""

import json
import logging


def extract_data_from_json(file_path):
    """Extract data from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            logging.info("Data successfully extracted from %s.", file_path)
            return data
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"{file_path} not found.") from exc


def load_data_to_json(data, file_path):
    """Save data to a JSON file."""

    with open(file_path, "r", encoding="utf-8") as json_file:
        json.dump(data, json_file)
        logging.info("Data successfully saved: %s.", file_path)


def extract_data_from_file(file_path):
    """Read file using readlines()"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.readlines()
            logging.info("Data successfully extracted from %s.", file_path)
            return data
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"{file_path} not found.") from exc
