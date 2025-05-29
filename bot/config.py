import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
CREDS_FILE = os.getenv("GOOGLE_CREDS_JSON")
SHEET_NAME = os.getenv("SHEET_NAME")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
