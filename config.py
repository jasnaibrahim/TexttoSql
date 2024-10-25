import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
