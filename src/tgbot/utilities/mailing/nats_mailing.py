import msgpack
import nats
from nats.aio.client import Client
from nats.js import JetStreamContext

from src.common.config.nats import NatsConfig
from src.infra import dto


class NatsMailing:
    def __init__(self):
        self.nc: Client | None = None
        self.js: JetStreamContext | None = None
        self.host = NatsConfig.compose().host

    async def connect(self):
        self.nc = await nats.connect(self.host)
        self.js = self.nc.jetstream()
        await self.js.add_stream(name="mailingtg", subjects=["mailing"])

    async def start_mailing(self, message: str, users: list[dto.UserDTO]) -> None:
        for user in users:
            await self.js.publish("mailing", msgpack.packb(message), headers={"user_id": str(user.id)})

    async def close(self):
        await self.nc.close()
