import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

MIN_SAMPLES_FOR_TRAINING = 10
CONTAMINATION = 0.05
RANDOM_STATE = 42