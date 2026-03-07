from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_db: str = "cabazes"
    postgres_user: str = "cabazes_user"
    postgres_password: str = "change_me"
    postgres_host: str = "db"
    postgres_port: int = 5432
    jwt_secret: str = "change_me"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
