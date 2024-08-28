"""
Module for loading environment settings and setting API base URL based on the current environment.
"""

import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.learn.mit.edu")
API_URL = f"{API_BASE_URL}/api/v1/courses/?platform=ocw"
