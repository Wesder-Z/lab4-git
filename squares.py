"""Вычисление квадратов чисел с помощью map."""


def squares_one_to_ten() -> list[int]:
    """Возвращает квадраты всех целых чисел от 1 до 10."""
    return list(map(lambda number: number**2, range(1, 11)))
