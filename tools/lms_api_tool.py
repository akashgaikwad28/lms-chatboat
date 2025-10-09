import os
import json
import requests
import traceback
from langchain.tools import tool
from utils.logger import get_logger

logger = get_logger(name="lms_api_tool")

SAMPLE_COURSES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_courses.json")
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
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- RequestException in get_available_courses ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"-----------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ Unable to fetch courses right now."

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in get_available_courses ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"-------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
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
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- RequestException in get_course_details ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"----------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ Failed to fetch course details."

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in get_course_details ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ An error occurred while retrieving course details."
