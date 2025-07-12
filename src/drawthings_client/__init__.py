"""
Draw Things client library and CLI tool
"""

__version__ = "0.1.0"


def hello() -> str:
    return "Hello from drawthings-client!"


# 公開API
__all__ = [
    "hello",
    "__version__",
]
