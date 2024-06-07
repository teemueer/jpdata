import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))
    DATABASE_NAME = "jpdata"
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql:///{Config.DATABASE_NAME}-dev"

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = f"postgresql:///{Config.DATABASE_NAME}-test"

class ProductionConfig(Config):
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
