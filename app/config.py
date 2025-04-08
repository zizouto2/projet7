from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_name: str = "google/gemma-3-1b-it"
    serpapi_key: str = ""
    class Config:
        env_file = ".env"

settings = Settings()
