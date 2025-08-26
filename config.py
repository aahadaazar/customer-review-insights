import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

    # Validation
    if not OPENAI_API_KEY:
        logging.warning("OPENAI_API_KEY not set. Please add it to your .env file")
    if not SUPABASE_URL:
        logging.warning("SUPABASE_URL not set. Please add it to your .env file")
    if not SUPABASE_SERVICE_KEY:
        logging.warning("SUPABASE_SERVICE_KEY not set. Please add it to your .env file")
