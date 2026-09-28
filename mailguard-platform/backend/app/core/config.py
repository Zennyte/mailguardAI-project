from pydantic_settings import BaseSettings, SettingsConfigDict


# Konfigurimi i aplikacionit, lexohet nga .env
class Settings(BaseSettings):
    # Konfigurimi lexohet nga skedari .env
    APP_NAME: str = "MailGuard AI Platform"
    APP_ENV: str = "development"

    SECRET_KEY: str = "change-this-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mailguard_platform"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "mailguard_platform"

    FRONTEND_URL: str = "http://localhost:5173"

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
