from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_ENV: str
    CLIENT_HOST: str
    CLIENT_ACCOUNT_ACTIVATION_URL: str
    DATABASE_URL: str
    SMTP_SERVER: str
    SMTP_SENDER_MAIL: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: str
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()