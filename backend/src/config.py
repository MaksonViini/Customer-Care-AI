import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings, Field

load_dotenv()


class TestConfig(BaseSettings):
    env: Literal["test"]
    db_host: str = Field(env="DB_HOST_TEST")
    db_password: str = Field(env="DB_PASSWORD_TEST")
    db_database: str = Field(env="DB_DATABASE_TEST")
    db_port: str = Field(env="DB_PORT_TEST")


class ProdConfig(BaseSettings):
    env: Literal["prod"]
    db_host: str = Field(env="DB_HOST_PROD")
    db_password: str = Field(env="DB_PASSWORD_PROD")
    db_database: str = Field(env="DB_DATABASE_PROD")
    db_port: str = Field(env="DB_PORT_PROD")


class DevConfig(BaseSettings):
    env: Literal["dev"]
    db_host: str = Field(env="DB_HOST_DEV")
    db_password: str = Field(env="DB_PASSWORD_DEV")
    db_database: str = Field(env="DB_DATABASE_DEV")
    db_port: str = Field(env="DB_PORT_DEV")
    db_user: str = Field(env="DB_USER")


class Settings(BaseModel):
    config: DevConfig | ProdConfig | TestConfig


def get_settings() -> Settings:
    """Gets the settings for the current environment."""
    env = os.getenv("ENV")
    if env == "test":
        return TestConfig()
    elif env == "prod":
        return ProdConfig()
    elif env == "dev":
        return DevConfig()
    else:
        raise ValueError("Unknown environment")


settings = get_settings()


def get_db_url() -> str:
    """Gets the URL of the database."""
    db_host = settings.db_host
    db_password = settings.db_password
    db_database = settings.db_database
    db_port = settings.db_port
    db_user = settings.db_user

    return f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
