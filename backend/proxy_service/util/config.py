import os

from dotenv import load_dotenv

load_dotenv(override=False)

AUTH_URL = os.getenv("AUTH_URL", "http://auth_service:8000")
USER_URL = os.getenv("USER_URL", "http://user_service:8000")
GOAL_URL = os.getenv("GOAL_URL", "http://goal_service:8000")
TASK_URL = os.getenv("TASK_URL", "http://task_service:8000")
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", "http://notification_service:8000")
CALENDAR_URL = os.getenv("CALENDAR_URL", "http://calendar_service:8000")
