import os
from dotenv import load_dotenv

load_dotenv() # handles searching for .env file and gracefully handles if it doesn't exist

DB_PATH = os.getenv("DB_PATH", "database.db")

