from dataclasses import dataclass

from environs import Env
from sqlalchemy import URL
from typing_extensions import Self


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @classmethod
    def compose(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            host=env.str('DB_HOST'),
            port=env.str('DB_PORT'),
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            database=env.str('DB_NAME'),
        )

    @property
    def sqlalchemy_uri(self) -> URL:
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
