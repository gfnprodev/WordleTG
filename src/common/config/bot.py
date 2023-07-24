from dataclasses import dataclass
from typing import Self

from environs import Env


@dataclass
class BotConfig:
    bot_token: str
    admins: list

    @classmethod
    def compose(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            bot_token=env.str("BOT_TOKEN"),
            admins=[int(value) for value in env.list("ADMINS")],
        )
