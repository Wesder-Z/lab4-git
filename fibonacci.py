"""Генератор последовательности Фибоначчи."""

from collections.abc import Iterator


def fibonacci(count: int) -> Iterator[int]:
    """Генерирует заданное количество чисел Фибоначчи.

    Args:
        count: Количество чисел, начиная с нуля.

    Yields:
        Очередное число последовательности Фибоначчи.

    Raises:
        TypeError: Если количество не является целым числом.
        ValueError: Если количество отрицательное.
    """
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("Количество должно быть целым числом")
    if count < 0:
        raise ValueError("Количество не может быть отрицательным")

    current = 0
    following = 1

    for _ in range(count):
        yield current
        current, following = following, current + following
