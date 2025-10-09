
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --------- Logging Setup ---------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# --------- Token Management (Optional) ---------
def get_bearer_token():
    """
    Retrieves the bearer token from environment variable or session store.
    """
    token = os.getenv("LMS_ACCESS_TOKEN")  # Ideally use a secure vault or login flow
    if not token:
        logger.warning("LMS_ACCESS_TOKEN not found in environment.")
    return token


# --------- JSON File Loader ---------
def load_json_file(filepath):
    """
    Loads and returns JSON data from a file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Failed to load JSON file: {filepath} | Error: {e}")
        return None


# --------- Course Formatter ---------
def format_course(course):
    """
    Format a course dictionary into a readable string for LLM response.
    """
    return (
        f"📘 **{course.get('title')}**\n"
        f"Category: {course.get('category')} | Level: {course.get('level')}\n"
        f"Language: {course.get('primaryLanguage')} | Price: ${course.get('pricing', 0)}\n"
        f"Description: {course.get('description')}\n"
    )


# --------- Timestamp ---------
def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --------- API Headers with Auth ---------
def get_auth_headers():
    """
    Return headers with Authorization if token is available.
    """
    token = get_bearer_token()
    headers = {
        "Content-Type": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers
