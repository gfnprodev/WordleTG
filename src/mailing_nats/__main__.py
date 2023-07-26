import asyncio

import nats
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from msgpack import unpackb
from nats.aio.msg import Msg

from src.common.config.bot import BotConfig
from src.common.config.nats import NatsConfig
from src.tgbot.misc.helpers import get_bot_instance
from nats.errors import TimeoutError


async def main():
    host = NatsConfig.compose().host
    nc = await nats.connect(host)
    js = nc.jetstream()
    await js.add_stream(name="mailingtg", subjects=["mailing"])
    psub = await js.pull_subscribe(stream="mailingtg", subject="mailing", durable="aiogram")
    token = BotConfig.compose()
    bot = get_bot_instance(token.bot_token)
    if not psub:
        "error"
    else:
        cant_send = 0
        while True:
            try:
                msgs: list[Msg] = await psub.fetch(5)
                for msg in msgs:
                    user_id = int(msg.headers['user_id'])
                    msg_unpacked = unpackb(msg.data)
                    try:
                        await bot.send_message(user_id, msg_unpacked)
                    except TelegramForbiddenError:
                        cant_send += 1
                        pass
                    await msg.ack()
            except TimeoutError:
                await asyncio.sleep(5)
            except TelegramRetryAfter as e:
                await asyncio.sleep(float(e.retry_after))
                continue
    await bot.session.close()
    await nc.close()

try:
    asyncio.run(main())
except (SystemExit, KeyboardInterrupt):
    pass
