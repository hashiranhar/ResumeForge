from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    password_reset_token_expire_minutes: int = 60
    environment: str = "development"
    
    huggingface_api_key: str
    llm_model: str = "deepseek-ai/DeepSeek-V3-0324"
    llm_max_tokens: int = 2000
    llm_temperature: float = 0.7
    
    class Config:
        env_file = "../.env"

settings = Settings()
