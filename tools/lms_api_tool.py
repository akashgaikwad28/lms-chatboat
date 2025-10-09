# tools/lms_api_tool.py

import os
import logging
import requests
from langchain.tools import tool
import json


## for testing 
SAMPLE_COURSES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_courses.json") 

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LMS_BASE_URL = os.getenv("LMS_API_BASE_URL")

@tool
def get_available_courses() -> str:
    """Fetch a list of available courses from the LMS."""
    
    
    try:
        if not LMS_BASE_URL:
            logger.error("LMS_API_BASE_URL is not set.")
            return "❌ LMS API URL not configured."

        url = f"{LMS_BASE_URL}/student/course/get"
        logger.info(f"Requesting available courses from: {url}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            logger.warning("LMS API responded with success=False.")
            return "❌ Failed to fetch courses."

        courses = data.get("data", [])
        if not courses:
            logger.info("No courses found in LMS API response.")
            return "No courses available at the moment."

        result = "\n".join([
            f"- {course.get('title', 'Unknown')} (${course.get('pricing', 'N/A')})"
            for course in courses
        ])

        logger.info("Successfully fetched available courses.")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error when fetching courses: {e}", exc_info=True)
        return "⚠️ Unable to fetch courses right now."

    except Exception as e:
        logger.error(f"Unexpected error in get_available_courses: {e}", exc_info=True)
        return "⚠️ Something went wrong while fetching courses."

@tool
def get_course_details(course_id: str) -> str:
    """Get detailed information about a specific course using its ID."""
    try:
        if not LMS_BASE_URL:
            logger.error("LMS_API_BASE_URL is not set.")
            return "❌ LMS API URL not configured."

        url = f"{LMS_BASE_URL}/student/course/get/details/{course_id}"
        logger.info(f"Requesting course details from: {url}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            logger.warning(f"Course ID {course_id} not found.")
            return f"❌ Could not find course with ID {course_id}."

        course = data.get("data", {})
        formatted = (
            f"📘 {course.get('title', 'N/A')}\n"
            f"💰 Price: ${course.get('pricing', 'N/A')}\n"
            f"🎯 Level: {course.get('level', 'N/A')}\n"
            f"🗣️ Language: {course.get('primaryLanguage', 'N/A')}\n"
            f"📄 Description: {course.get('description', 'No description.')}"
        )

        logger.info(f"Successfully fetched details for course ID {course_id}")
        return formatted

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error when fetching course details: {e}", exc_info=True)
        return "⚠️ Failed to fetch course details."

    except Exception as e:
        logger.error(f"Unexpected error in get_course_details: {e}", exc_info=True)
        return "⚠️ An error occurred while retrieving course details."




# tools/lms_api_tool.py

# import json
# import logging

# async def get_available_courses(tool_input: str = "") -> list:
#     """Fetch available courses from local JSON dummy data."""
#     try:
#         file_path = "data/sample_courses.json"
#         with open(file_path, "r") as file:
#             courses = json.load(file)
#         logging.info("✅ Loaded courses from local file.")
#         return courses

#     except Exception as e:
#         logging.error(f"❌ Failed to load course data: {e}")
#         return []
