"""Фильтрация и преобразование данных из CSV-файла."""

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StudentResult:
    """Результат студента после преобразования данных CSV."""

    name: str
    score: int


def _row_to_result(row: dict[str, str]) -> StudentResult:
    """Преобразует строку CSV в типизированный результат."""
    try:
        name = row["name"].strip().title()
        score = int(row["score"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Некорректная строка CSV") from error

    if not name:
        raise ValueError("Имя студента не должно быть пустым")
    if not 0 <= score <= 100:
        raise ValueError("Оценка должна находиться в диапазоне от 0 до 100")

    return StudentResult(name=name, score=score)


def successful_students(
    file_path: str | Path,
    minimum_score: int = 60,
) -> list[StudentResult]:
    """Читает CSV и возвращает результаты не ниже заданного порога.

    Преобразование строк выполняется через ``map``, фильтрация результатов
    выполняется через ``filter``.

    Args:
        file_path: Путь к CSV-файлу со столбцами ``name`` и ``score``.
        minimum_score: Минимальная проходная оценка от 0 до 100.

    Returns:
        Отфильтрованные результаты с оформленными именами и числовыми оценками.

    Raises:
        TypeError: Если проходная оценка не является целым числом.
        ValueError: Если порог или содержимое CSV некорректны.
    """
    if isinstance(minimum_score, bool) or not isinstance(minimum_score, int):
        raise TypeError("Проходная оценка должна быть целым числом")
    if not 0 <= minimum_score <= 100:
        raise ValueError("Проходная оценка должна быть от 0 до 100")

    with open(file_path, encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {"name", "score"}
        if reader.fieldnames is None or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV должен содержать столбцы name и score")

        transformed = map(_row_to_result, reader)
        passed = filter(
            lambda student: student.score >= minimum_score,
            transformed,
        )
        return list(passed)
