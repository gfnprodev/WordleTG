from _operator import attrgetter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infra.database.dao.holder import HolderDAO


async def get_users_top_getter(dao: "HolderDAO", **kwargs):
    users = await dao.user.get_all_users()
    users.sort(key=attrgetter("rating"), reverse=True)
    users = users[:10]
    result = "\n".join([f"⭐ {user.username} - {user.rating} ELO" for user in users])
    return {"top": result}
