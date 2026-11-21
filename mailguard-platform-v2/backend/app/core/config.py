from pydantic_settings import BaseSettings, SettingsConfigDict


# Konfigurimi i aplikacionit - vlerat lexohen nga skedari .env
class Settings(BaseSettings):
    APP_NAME: str = "MailGuard AI Platform"
    APP_ENV: str = "development"

    # JWT
    SECRET_KEY: str = "change-this-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Tokenat ruhen ne cookie "httpOnly" (JavaScript nuk i lexon dot).
    # Vendose True kur faqja sherbehet me HTTPS (production); ne zhvillim lokal (http) duhet False.
    COOKIE_SECURE: bool = False

    # Databazat
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mailguard_platform"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "mailguard_platform"

    # Adresa e frontend-it (per CORS)
    FRONTEND_URL: str = "http://localhost:5173"

    # Shpjegimi AI i rezultatit (opsional - pa API key thjesht nuk shfaqet)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
