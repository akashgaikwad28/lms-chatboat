import os
import json
import requests
import traceback
from utils.logger import get_logger

logger = get_logger(name="lms_api_tool")

LMS_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:5000")  # Default to local LMS

def load_course_data() -> list:
    """
    Load course data from the LMS backend API.
    Fallback to empty list if request fails or LMS is down.
    """
    try:
        logger.info(f"Fetching course data from {LMS_BASE_URL}/student/course/get")
        response = requests.get(f"{LMS_BASE_URL}/student/course/get", timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("success") and "data" in data:
            logger.info(f"Successfully loaded {len(data['data'])} courses from LMS API.")
            return data["data"]
        else:
            logger.warning("LMS API response received but marked unsuccessful.")
            return []

    except requests.RequestException as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        log_message = (
            f"\n--- LMS API Exception ---\n"
            f"File          : {tb.filename}\n"
            f"Function      : {tb.name}\n"
            f"Line No       : {tb.lineno}\n"
            f"Error Type    : {type(e).__name__}\n"
            f"Error Message : {str(e)}\n"
            f"--------------------------\n"
        )
        logger.error(log_message)
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return []


# SAMPLE_JSON_PATH = os.path.join("data", "sample_courses.json")

# def load_course_data(json_path: str = SAMPLE_JSON_PATH) -> list:
#     try:
#         logger.info(f"Loading course data from local file: {json_path}")
#         if not os.path.exists(json_path):
#             logger.error(f"File not found: {json_path}")
#             return []

#         with open(json_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         if not isinstance(data, list):
#             logger.warning(f"Invalid data format in {json_path}. Expected a list.")
#             return []

#         logger.info(f"Loaded {len(data)} courses from local test file.")
#         return data

#     except Exception as e:
#         tb = traceback.extract_tb(e.__traceback__)[-1]
#         log_message = (
#             f"\n--- Local JSON Exception ---\n"
#             f"File          : {tb.filename}\n"
#             f"Function      : {tb.name}\n"
#             f"Line No       : {tb.lineno}\n"
#             f"Error Type    : {type(e).__name__}\n"
#             f"Error Message : {str(e)}\n"
#             f"-----------------------------\n"
#         )
#         logger.error(log_message)
#         logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
#         return []
