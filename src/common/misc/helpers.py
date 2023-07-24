from typing import Any

import orjson


def orjson_dumps(v: Any, *, default: Any = ...) -> str:
    return orjson.dumps(v, default=default).decode()