"""
Module for interacting with the MIT OpenCourseWare API.
"""
import math
import logging
import requests
from retry import retry
from tqdm import tqdm

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@retry(tries=3, delay=2, logger=logger)
def make_request(next_page, page_size):
    """
    Make a request to the API with retry logic.
    """
    return requests.get(next_page, params={"limit": page_size}, timeout=60)


def paginated_response(api_url, page_size=100):
    """
    Generate paginated responses from the API.
    """
    next_page = api_url
    while next_page:
        response = make_request(next_page, page_size)
        data = response.json()
        next_page = data.get("next")
        yield data


def extract_data_from_api(api_url):
    """Extract all data from the MIT OpenCourseWare API."""
    page_size = 100
    pages = paginated_response(api_url, page_size)

    first_page = next(pages)
    api_data = first_page.get("results", [])
    total_pages = math.ceil(first_page["count"] / page_size)

    # Remaining pages
    for page in tqdm(
        pages,
        desc="Loading data from MIT OCW API",
        total=total_pages - 1,
    ):
        page_results = page.get("results", [])
        api_data.extend(page_results)

    return api_data
