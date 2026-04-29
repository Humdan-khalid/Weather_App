from dotenv import load_dotenv
import os

load_dotenv()

secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")
weather_api_key=os.getenv("WEATHER_API_KEY")
url=os.getenv("URL")
database_url=os.getenv("DATABASE_URL")
