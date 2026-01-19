import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")
# Selecting env file based on running environment (production or development)
if ENV == 'production':
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

# Database variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SCHEMA = os.getenv("DB_SCHEMA")

# Middleware variables
CORS_ORIGINS = os.getenv('CORS_ORIGIN').split(',') if os.getenv('CORS_ORIGIN') else []