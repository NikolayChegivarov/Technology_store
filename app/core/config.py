from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # security
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # База данных
    HOST_DB: str
    USER_DB: str
    PASSWORD_DB: str
    PORT_DB: int
    NAME_DB: str

    class Config:
        env_file = ".env"


settings = Settings()
