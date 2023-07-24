from dataclasses import dataclass
from typing import Self

from environs import Env

from src.common.config.bot import BotConfig
from src.common.config.db import DbConfig
from src.common.config.misc import MiscConfig
from src.common.config.redis import RedisConfig


@dataclass
class Config:
    db: DbConfig
    misc: MiscConfig
    bot: BotConfig
    redis: RedisConfig

    @classmethod
    def from_env(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            db=DbConfig.compose(env),
            misc=MiscConfig.compose(env),
            bot=BotConfig.compose(env),
            redis=RedisConfig.compose(env),
        )
