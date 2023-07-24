from dataclasses import dataclass
from typing import Self

from environs import Env


@dataclass
class MiscConfig:
    log_level: int
    use_redis: bool

    @classmethod
    def compose(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            log_level=env.log_level('LOG_LEVEL'),
            use_redis=env.bool("USE_REDIS")
        )