import os
from dotenv import load_dotenv

load_dotenv()

PLIVO_AUTH_ID = os.getenv("PLIVO_AUTH_ID")
PLIVO_AUTH_TOKEN = os.getenv("PLIVO_AUTH_TOKEN")
PLIVO_FROM_NUMBER = os.getenv("PLIVO_FROM_NUMBER")
PLIVO_TO_NUMBER = os.getenv("PLIVO_TO_NUMBER")
PLIVO_ASSOCIATE_NUMBER = os.getenv("PLIVO_ASSOCIATE_NUMBER")
OTP_CODE = os.getenv("OTP_CODE", "1503")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
AUDIO_MP3_URL = os.getenv("AUDIO_MP3_URL", "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
