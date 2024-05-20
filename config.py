from pydantic_settings import BaseSettings
from pydantic import EmailStr
from pathlib import Path


class Settings(BaseSettings):
    # database related
    db_host: str
    db_port: int
    db_name: str
    db_pwd: str
    db_usr: str
    db_name: str
    port: str

    # JWT Token Related
    secret_key: str
    refresh_secret_key: str
    algorithm: str
    timeout: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    #
    # # internal env
    adminapikey: str
    # mqtt settings
    mqtt_host: str
    mqtt_port: int
    mqtt_username: str
    mqtt_password: str
    #
    # SERVER: str
    MAIL_HOST: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool
    MAIL_SSL: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool
    MAIL_FROM: EmailStr

    class Config:
        env_file = Path(__file__).resolve().parent / ".env"
        print(f'environment created - {Path(Path(__file__).resolve().name)}')


setting = Settings()
