"""
Module to interact with MIT OpenCourseWare API and write data to a JSON file.
"""
import json
import logging

from .constants import API_URL
from .client import extract_data_from_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_json(output_file="ocw_api_data.json"):
    """Fetches data from MIT OpenCourseWare API and writes it to a JSON file."""
    api_data = extract_data_from_api(api_url=API_URL)
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(api_data, json_file, ensure_ascii=False, indent=4)
        logger.info("Data saved to %s at present directory.", output_file)
    except IOError as e:
        logger.error("Error saving data to JSON: %s", e)
