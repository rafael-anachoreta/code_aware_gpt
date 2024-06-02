import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Set debug flag
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

def debug_print(message):
    if DEBUG:
        print(message)

# Define the target directory
target_directory = os.getenv('TARGET_DIRECTORY')
