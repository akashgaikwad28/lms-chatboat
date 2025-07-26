# tools/lms_api_tool.py

from langchain.tools import tool
import requests
import os

LMS_BASE_URL = os.getenv("LMS_API_BASE_URL")

@tool
def get_available_courses() -> str:
    """Fetch a list of available courses from the LMS."""
    try:
        response = requests.get(f"{LMS_BASE_URL}/student/course/get")
        data = response.json()

        if not data.get("success"):
            return "❌ Failed to fetch courses."

        courses = data.get("data", [])
        if not courses:
            return "No courses available at the moment."

        return "\n".join([f"- {course['title']} (${course['pricing']})" for course in courses])

    except Exception as e:
        print("LMS Tool Error:", e)
        return "⚠️ Unable to fetch courses right now."

@tool
def get_course_details(course_id: str) -> str:
    """Get detailed information about a specific course using its ID."""
    try:
        response = requests.get(f"{LMS_BASE_URL}/student/course/get/details/{course_id}")
        data = response.json()

        if not data.get("success"):
            return f"❌ Could not find course with ID {course_id}."

        course = data.get("data", {})
        return (
            f"📘 {course['title']}\n"
            f"💰 Price: ${course['pricing']}\n"
            f"🎯 Level: {course['level']}\n"
            f"🗣️ Language: {course['primaryLanguage']}\n"
            f"📄 Description: {course['description']}"
        )

    except Exception as e:
        print("LMS Tool Error:", e)
        return "⚠️ Failed to fetch course details."
