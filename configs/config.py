# configs/config.py
import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")
# Selecting env file based on running environment (production or development)
match ENV:
    case "development":
        load_dotenv(".env.development")
    case "production":
        load_dotenv(".env.production")
    case _ if ENV.startswith("test"):
        load_dotenv(".env.test")

# Database variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SCHEMA = os.getenv("DB_SCHEMA")
# JWT Variables
JWT_TOKEN_LIFETIME = int(os.getenv("JWT_TOKEN_LIFETIME", 60))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Middleware variables
CORS_ORIGINS = os.getenv("CORS_ORIGIN").split(",") if os.getenv("CORS_ORIGIN") else []
