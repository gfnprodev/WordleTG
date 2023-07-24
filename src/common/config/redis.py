from dataclasses import dataclass
from typing import Self

from environs import Env


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str

    @classmethod
    def compose(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            host=env.str("REDIS_HOST"),
            port=env.int("REDIS_PORT"),
            password=env.str("REDIS_PASSWORD")
        )
