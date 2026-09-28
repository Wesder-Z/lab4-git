"""Декораторы для логирования и повторения вызовов."""

import logging
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

LOGGER = logging.getLogger(__name__)


def log_calls(function: Callable[P, R]) -> Callable[P, R]:
    """Добавляет сообщения журнала до и после вызова функции."""

    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        LOGGER.info("Вызов функции %s", function.__name__)
        result = function(*args, **kwargs)
        LOGGER.info("Функция %s завершена", function.__name__)
        return result

    return wrapper


def repeat(times: int) -> Callable[[Callable[P, R]], Callable[P, list[R]]]:
    """Создаёт декоратор для многократного вызова функции.

    Args:
        times: Положительное количество вызовов.

    Returns:
        Декоратор, возвращающий список результатов всех вызовов.

    Raises:
        TypeError: Если количество не является целым числом.
        ValueError: Если количество меньше единицы.
    """
    if isinstance(times, bool) or not isinstance(times, int):
        raise TypeError("Количество повторов должно быть целым числом")
    if times < 1:
        raise ValueError("Количество повторов должно быть положительным")

    def decorator(function: Callable[P, R]) -> Callable[P, list[R]]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> list[R]:
            return [function(*args, **kwargs) for _ in range(times)]

        return wrapper

    return decorator
