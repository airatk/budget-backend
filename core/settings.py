from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    JWT_ALGORITHM: str
    JWT_ACCESS_SECRET_KEY: str

    POSTGRES_DRIVER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str

    POSTGRES_URL: PostgresDsn | None

    @validator("POSTGRES_URL", pre=True)
    def assemble_postgres_dsn(cls, value: str | None, values: dict[str, Any]) -> str:  # noqa: N805, WPS110
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme=values.get("POSTGRES_DRIVER"),
            user=values.get("POSTGRES_USERNAME"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path="/{0}".format(values.get("POSTGRES_DATABASE")),
        )


settings: Settings = Settings(_env_file="configurations/.env")
