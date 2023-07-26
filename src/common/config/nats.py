from dataclasses import dataclass
from typing import Self

from environs import Env


@dataclass
class NatsConfig:
    host: str

    @classmethod
    def compose(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            host=env.str("NATS_HOST"),
        )
