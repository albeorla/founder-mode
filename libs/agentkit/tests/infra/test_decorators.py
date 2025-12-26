import asyncio

import pytest
from agentkit.infra.decorators import logged, with_fallback, with_retry, with_timeout


@logged()
def sync_func(x: int) -> int:
    return x + 1


@logged()
async def async_func(x: int) -> int:
    await asyncio.sleep(0.01)
    return x + 1


def test_logged_decorator() -> None:
    assert sync_func(1) == 2


@pytest.mark.asyncio
async def test_logged_decorator_async() -> None:
    assert await async_func(1) == 2


@with_fallback(fallback=42)
def sync_fail() -> int:
    raise ValueError("fail")


@with_fallback(fallback=42)
async def async_fail() -> int:
    raise ValueError("fail")


def test_with_fallback() -> None:
    assert sync_fail() == 42


@pytest.mark.asyncio
async def test_with_fallback_async() -> None:
    assert await async_fail() == 42


retry_count = 0


@with_retry(max_attempts=3)
def sync_retry() -> int:
    global retry_count
    retry_count += 1
    if retry_count < 3:
        raise ValueError("retry")
    return retry_count


@pytest.mark.asyncio
async def test_with_retry_sync() -> None:
    global retry_count
    retry_count = 0
    assert sync_retry() == 3


@with_timeout(seconds=0.1)
async def async_slow() -> str:
    await asyncio.sleep(0.5)
    return "done"


@pytest.mark.asyncio
async def test_with_timeout_async() -> None:
    with pytest.raises(asyncio.TimeoutError):
        await async_slow()
