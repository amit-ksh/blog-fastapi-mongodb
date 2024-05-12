import os
from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

import models


class Settings(BaseSettings):
    """App settings"""

    # database configurations
    DATABASE_URL: Optional[str] = os.environ.get("DATABASE_URL")

    # JWT
    secret_key: str = os.environ.get("SECRET_KEY", "secret")
    algorithm: str = "HS256"

    class Config:
        """Configurations"""

        env_file = ".env.dev"
        from_attributes = True


async def initiate_database():
    """Initiate database"""
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=models.__all__
    )
