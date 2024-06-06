import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))
    DATABASE_NAME = "jpdata"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql:///{Config.DATABASE_NAME}-dev"

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = f"postgresql:///{Config.DATABASE_NAME}-test"

config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "default": DevelopmentConfig,
}
