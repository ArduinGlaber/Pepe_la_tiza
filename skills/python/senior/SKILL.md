---
name: python-senior
description: >
  Advanced Python patterns for senior developers. Async, decorators, metaclasses, type hints, performance.
  Trigger: When writing Python code - advanced typing, async, performance, design patterns.
metadata:
  author: gentleman-ai
  version: "1.0"
---

## Senior Python Philosophy

Write code that the next developer understands in 5 minutes. Clarity over cleverness.

---

## Type Hints (REQUIRED)

Always use type hints. They're not optional.

```python
from typing import TypeVar, Generic, Protocol, Callable, Optional
from dataclasses import dataclass

T = TypeVar('T')

# ✅ Always type hints
def process_data(items: list[str], callback: Callable[[str], int]) -> dict[str, int]:
    return {item: callback(item) for item in items}

# ✅ Data classes for DTOs
@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime

# ✅ Generic types
class Repository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model
    
    def get(self, id: int) -> Optional[T]:
        ...

# ✅ Protocol for duck typing
class Serializer(Protocol):
    def serialize(self) -> bytes: ...
    def deserialize(self, data: bytes) -> Self: ...

# ✅ Literal for enum-like strings
from typing import Literal
Mode = Literal["debug", "release", "test"]
```

---

## Dataclasses (PREFERRED)

Use dataclasses for data structures. They handle `__init__`, `__repr__`, `__eq__`.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Config:
    host: str
    port: int = 8080
    debug: bool = False
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

# ✅ Auto-comparison
config1 = Config(host="localhost")
config2 = Config(host="localhost")
assert config1 == config2  # Works!

# ✅ Frozen for immutability
@dataclass(frozen=True)
class ImmutableConfig:
    host: str
    port: int
```

---

## Async/Await (REQUIRED for I/O)

Use `asyncio` for I/O-bound tasks. Never block the event loop.

```python
import asyncio
from typing import AsyncIterator

# ✅ Async context manager
class AsyncDatabase:
    async def __aenter__(self):
        self.conn = await connect_async()
        return self
    
    async def __aexit__(self, *args):
        await self.conn.close()
    
    async def fetch(self, query: str) -> list[dict]:
        return await self.conn.execute(query)

# Usage
async def main():
    async with AsyncDatabase() as db:
        results = await db.fetch("SELECT * FROM users")

# ✅ Async generator
async def stream_users() -> AsyncIterator[User]:
    async for row in db.stream("SELECT * FROM users"):
        yield User(**row)

# ✅ Run async from sync code
def run_async(coro):
    return asyncio.run(coro)
```

---

## Context Managers (REQUIRED)

Use context managers for resource management. RAII in Python.

```python
from contextlib import contextmanager

# ✅ Context manager for temporary state
@contextmanager
def temporary_debug(enabled: bool = True):
    old_value = debug_mode
    debug_mode = enabled
    try:
        yield
    finally:
        debug_mode = old_value

# Usage
with temporary_debug():
    do_something()

# ✅ Abstract base for classes
from abc import ABC, abstractmethod

class Cache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]: ...
    
    @abstractmethod
    async def set(self, key: str, value: bytes, ttl: int = 300) -> None: ...
```

---

## Decorators (Senior Level)

Decorators should preserve function metadata and be composable.

```python
import functools
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec('P')
T = TypeVar('T')

# ✅ Decorator with parameters
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (attempt + 1))
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2.0)
def unreliable_api_call() -> dict:
    ...

# ✅ Decorator that adds behavior
def log_calls(logger: Logger):
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            logger.debug(f"Calling {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} succeeded")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed: {e}")
                raise
        return wrapper
    return decorator
```

---

## Error Handling

Be explicit. Don't swallow exceptions. Use custom exceptions.

```python
# ✅ Custom exceptions hierarchy
class AppError(Exception):
    """Base exception for all app errors"""
    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationError(AppError):
    """Raised when input validation fails"""
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}", code="VALIDATION_ERROR")

class NotFoundError(AppError):
    """Raised when a resource is not found"""
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} not found: {id}", code="NOT_FOUND")

# ✅ Use exceptions for control flow (when appropriate)
def get_or_create(user_id: str) -> User:
    user = db.get(user_id)
    if user is None:
        raise NotFoundError("User", user_id)
    return user

# ✅ NEVER do this
try:
    do_something()
except:
    pass  # Swallowed!
```

---

## Performance Patterns

```python
import sys
from functools import lru_cache, cached_property
from collections.abc import Iterator

# ✅ LRU cache for expensive computations
@lru_cache(maxsize=1024)
def expensive_calculation(n: int) -> int:
    return n ** 2

# ✅ Cached property for computed attributes
class HeavyObject:
    @cached_property
    def expensive_data(self) -> list[dict]:
        return self._load_data()  # Only computed once

# ✅ Generator for memory efficiency
def process_large_file(filepath: str) -> Iterator[dict]:
    with open(filepath) as f:
        for line in f:
            yield parse_line(line)

# ✅ Batch processing
def batch_process(items: list[T], batch_size: int = 100) -> Iterator[list[T]]:
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
```

---

## Structuring Projects

```
src/
├── __init__.py
├── main.py              # Entry point
├── config.py            # Configuration
├── models/              # Data models (dataclasses, Pydantic)
│   ├── __init__.py
│   ├── user.py
│   └── order.py
├── services/             # Business logic
│   ├── __init__.py
│   ├── user_service.py
│   └── order_service.py
├── repositories/         # Data access
│   ├── __init__.py
│   └── user_repository.py
├── api/                  # API endpoints/routes
│   ├── __init__.py
│   └── v1/
├── core/                 # Shared utilities
│   ├── __init__.py
│   ├── exceptions.py
│   └── logging.py
└── tests/
    ├── unit/
    └── integration/
```

---

## Testing Patterns

```python
import pytest
from unittest.mock import Mock, AsyncMock, patch

# ✅ Unit test with fixtures
@pytest.fixture
def user_repository():
    repo = Mock()
    repo.get.return_value = User(id=1, name="Test")
    return repo

def test_get_user(user_repository):
    result = user_repository.get(1)
    assert result.name == "Test"
    user_repository.get.assert_called_once_with(1)

# ✅ Async test
@pytest.mark.asyncio
async def test_async_service():
    service = AsyncUserService()
    result = await service.get_user(1)
    assert result.id == 1

# ✅ Parametrized test
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

---

## Logging (REQUIRED)

```python
import logging
from typing import get_origin, get_type_hints

# ✅ Structured logging
logger = logging.getLogger(__name__)

logger.info(
    "User created",
    extra={
        "user_id": user.id,
        "email": user.email,
        "action": "user_create"
    }
)

# ✅ Child loggers for modules
logger = logging.getLogger(__name__)  # Gets module name automatically
```

---

## Environment & Config

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## Resources

- https://docs.python.org/3/library/typing.html
- https://realpython.com/async-io-python/
- https://docs.python-guide.org/
