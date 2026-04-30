from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VPN Control Plane"
    api_prefix: str = "/api/v1"
    jwt_secret: str = "change-me-in-prod"
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_prefix="VPN_", env_file=".env", extra="ignore")


settings = Settings()

