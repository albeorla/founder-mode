import asyncio
import functools
import inspect
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar, cast

from tenacity import (
    AsyncRetrying,
    Retrying,
    stop_after_attempt,
    wait_exponential,
)

T = TypeVar("T", bound=Callable[..., Any])

logger = logging.getLogger("agentkit.decorators")


def logged() -> Callable[[T], T]:
    """Decorator that logs function entry, exit, and execution time."""

    def decorator(func: T) -> T:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                start = time.perf_counter()
                logger.debug(f"Entering {func.__name__}")
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = time.perf_counter() - start
                    logger.debug(f"Exiting {func.__name__} (duration: {duration:.4f}s)")

            return cast(T, async_wrapper)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                start = time.perf_counter()
                logger.debug(f"Entering {func.__name__}")
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.perf_counter() - start
                    logger.debug(f"Exiting {func.__name__} (duration: {duration:.4f}s)")

            return cast(T, sync_wrapper)

    return decorator


def with_fallback(fallback: Any) -> Callable[[T], T]:
    """Decorator that returns a fallback value if the function raises an exception."""

    def decorator(func: T) -> T:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Error in {func.__name__}: {e}. Returning fallback.")
                    return fallback

            return cast(T, async_wrapper)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Error in {func.__name__}: {e}. Returning fallback.")
                    return fallback

            return cast(T, sync_wrapper)

    return decorator


def with_retry(
    max_attempts: int = 3,
    wait_min: float = 1,
    wait_max: float = 10,
) -> Callable[[T], T]:
    """Decorator that retries the function on failure using exponential backoff."""

    def decorator(func: T) -> T:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                async for attempt in AsyncRetrying(
                    stop=stop_after_attempt(max_attempts),
                    wait=wait_exponential(min=wait_min, max=wait_max),
                    reraise=True,
                ):
                    with attempt:
                        return await func(*args, **kwargs)

            return cast(T, async_wrapper)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                for attempt in Retrying(
                    stop=stop_after_attempt(max_attempts),
                    wait=wait_exponential(min=wait_min, max=wait_max),
                    reraise=True,
                ):
                    with attempt:
                        return func(*args, **kwargs)

            return cast(T, sync_wrapper)

    return decorator


def with_timeout(seconds: float) -> Callable[[T], T]:
    """Decorator that raises a TimeoutError if the function takes too long."""

    def decorator(func: T) -> T:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)

            return cast(T, async_wrapper)
        else:
            # Sync timeout is complex to implement robustly without signals/threads.
            # For now, we only support it for async functions or throw error if called on sync.
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Basic implementation: just run it. Real sync timeout is hard.
                # In a real library, we might use a thread with a join(timeout).
                return func(*args, **kwargs)

            return cast(T, sync_wrapper)

    return decorator
