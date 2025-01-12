from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_port: int = Field(env="DB_PORT") # type: ignore
    db_name: str = Field(env="DB_NAME") # type: ignore
    db_user: str = Field(env="DB_USER") # type: ignore
    db_pass: str = Field(env="DB_PASS") # type: ignore
    db_host: str = Field(env="DB_HOST") # type: ignore

    test_db_port: int = Field(env="DB_TEST_PORT") # type: ignore
    test_db_name: str = Field(env="DB_TEST_NAME") # type: ignore
    test_db_user: str = Field(env="DB_TEST_USER") # type: ignore
    test_db_host: str = Field(env="DB_TEST_HOST") # type: ignore
    test_db_pass: str = Field(env="DB_TEST_PASS") # type: ignore

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def test_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.test_db_user}:{self.test_db_pass}@{self.test_db_host}:{self.test_db_port}/{self.test_db_name}"

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore
