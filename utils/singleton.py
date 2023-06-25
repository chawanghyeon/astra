# type: ignore

from typing import Any


class Singleton(type):
    _instances: dict[type["Singleton"], "Singleton"] = {}

    def __call__(cls: type["Singleton"], *args: Any, **kwargs: Any) -> "Singleton":
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
