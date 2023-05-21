from pydantic import BaseSettings, Field, SecretStr


class PostgresSettings(BaseSettings):
    """Settings for postgres database."""

    USER: str = Field(
        description="Username of postgres user",
    )
    PASSWORD: SecretStr = Field(
        description="Password for postgres user",
    )
    DB: str = Field(
        description="Name of maintaining database",
    )
    HOST: str = Field(
        default="localhost",
        description="Host name of postgres db",
    )
    PORT: int = Field(
        default=5432,
        description="Port of postgres database",
    )

    class Config:  # noqa
        env_file = ".env"
        env_prefix = "POSTGRES_"
        frozen = True

    def get_database_url(self) -> str:
        """Parse environment params to database url."""
        return (
            "postgresql+asyncpg://"
            f"{self.USER}:{self.PASSWORD.get_secret_value()}"
            f"@{self.HOST}:{self.PORT}/{self.DB}"
        )
