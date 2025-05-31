from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
