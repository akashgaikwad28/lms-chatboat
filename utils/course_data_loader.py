# # utils/course_data_loader.py

import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

LMS_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:5000")  # Default to local LMS

def load_course_data() -> list:
    """
    Load course data from the LMS backend API.
    Fallback to empty list if request fails or LMS is down.
    """
    try:
        response = requests.get(f"{LMS_BASE_URL}/student/course/get", timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad status codes

        data = response.json()

        if data.get("success") and "data" in data:
            return data["data"]
        else:
            logger.warning("LMS API response received but marked unsuccessful.")
            return []

    except requests.RequestException as e:
        logger.error(f"Failed to load courses from LMS: {e}")
        return []









''''code for local testing purposes only, not used in production'''



# import os
# import json
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# SAMPLE_JSON_PATH = os.path.join("data", "sample_courses.json")

# def load_course_data(json_path: str = SAMPLE_JSON_PATH) -> list:
#     """
#     Load course data from a local JSON file for testing purposes.
    
#     Args:
#         json_path (str): Path to the local course data JSON file.
    
#     Returns:
#         list: A list of course dictionaries.
#     """
#     try:
#         if not os.path.exists(json_path):
#             logger.error(f"File not found: {json_path}")
#             return []

#         with open(json_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         if not isinstance(data, list):
#             logger.warning(f"Invalid data format in {json_path}. Expected a list of courses.")
#             return []

#         logger.info(f"Loaded {len(data)} courses from local test file.")
#         return data

#     except Exception as e:
#         logger.exception(f"Failed to load course data from {json_path}")
#         return []
