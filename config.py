import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "buvi@2006"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "dash_auth"),
}

SESSION_CONFIG = {
    "SESSION_TYPE": "filesystem",
    "SESSION_PERMANENT": False,
    "SESSION_USE_SIGNER": True,
    "SESSION_KEY_PREFIX": "dashapp_",
    "SECRET_KEY": "your_secret_key",
}