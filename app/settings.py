import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    s3: bool = False

    password: str = os.getenv('PASSWORD', 'password')


settings = Settings()
