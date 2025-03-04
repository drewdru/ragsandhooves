from redis import Redis

from typing import Annotated
from collections.abc import Generator
from contextlib import contextmanager

from fastapi import Depends

from app.core.config import settings

def get_redis() -> Redis:
    return Redis(host=settings.REDIS_HOST, db=0, password=settings.REDIS_PASSWORD, decode_responses=True)

RedisDep = Annotated[Redis, Depends(get_redis)]
