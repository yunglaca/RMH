from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #database
    db_port: int = Field(env="DB_PORT")
    db_name: str = Field(env="DB_NAME")
    db_user: str = Field(env="DB_USER")
    db_pass: str = Field(env="DB_PASS")
    db_host: str = Field(env="DB_HOST")

    @property
    def database_url(self) -> str:
                return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"

settings = Settings()