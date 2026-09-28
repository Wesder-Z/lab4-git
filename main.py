"""Демонстрация заданий лабораторной работы №4."""

import logging
from pathlib import Path

from csv_processor import successful_students
from decorators import log_calls, repeat
from fibonacci import fibonacci
from squares import squares_one_to_ten


@log_calls
def add(left: int, right: int) -> int:
    """Складывает два целых числа."""
    return left + right


@repeat(3)
def greeting(name: str) -> str:
    """Формирует приветствие."""
    return f"Привет, {name}!"


def main() -> None:
    """Последовательно показывает результаты всех заданий."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("Квадраты чисел 1-10:", squares_one_to_ten())
    print("Первые 10 чисел Фибоначчи:", list(fibonacci(10)))
    print("Результат функции с логированием:", add(7, 5))
    print("Декоратор с параметром:", greeting("Анатолий"))

    csv_path = Path(__file__).with_name("data") / "students.csv"
    print("Результаты с оценкой не ниже 60:")
    for student in successful_students(csv_path):
        print(f"{student.name}: {student.score}")


if __name__ == "__main__":
    main()
