import os
from dataclasses import dataclass

@dataclass
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-jwt")
    JWT_EXP_MIN: int = int(os.getenv("JWT_EXP_MIN", "120"))
    HF_API_URL: str = os.getenv("HF_API_URL", "https://api-inference.huggingface.co/models/ibm-granite/granite-8b-instruct")
    HF_TOKEN: str = os.getenv("HUGGINGFACE_API_TOKEN", "")

settings = Settings()