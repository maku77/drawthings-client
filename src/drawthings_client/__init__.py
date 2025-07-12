"""
Draw Things client library and CLI tool
"""

from .client import DrawThingsClient

__version__ = "0.0.1"


def hello() -> str:
    return "Hello from drawthings-client!"


# 公開API
__all__ = [
    "DrawThingsClient",
    "hello",
    "__version__",
]
