from datetime import timedelta
import re
from typing import Any
 
def parse_list_env(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

def parse_expire(expire_str: str) -> timedelta:
    match = re.match(r"(\d+)(ms|s|m|h|d)$", expire_str.strip().lower())
    if not match:
        raise ValueError("Invalid expire format. Use '1d', '5m', '30s', '1h', '500ms'.")
    value, unit = int(match.group(1)), match.group(2)
    if unit == "ms":
        return timedelta(milliseconds=value)
    elif unit == "s":
        return timedelta(seconds=value)
    elif unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    else:
        raise ValueError("Unsupported time unit. Use 'ms', 's', 'm', or 'h'.")
