"""Модульные тесты функциональных заданий лабораторной работы №4."""

import tempfile
import unittest
from pathlib import Path

from csv_processor import StudentResult, successful_students
from decorators import log_calls, repeat
from fibonacci import fibonacci
from squares import squares_one_to_ten

DATA_FILE = Path(__file__).parents[1] / "data" / "students.csv"


class SquaresTests(unittest.TestCase):
    """Проверки вычисления квадратов через map."""

    def test_builds_squares_for_full_range_from_one_to_ten(self) -> None:
        expected = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

        self.assertEqual(squares_one_to_ten(), expected)


class FibonacciTests(unittest.TestCase):
    """Проверки генератора Фибоначчи."""

    def test_generates_first_ten_numbers(self) -> None:
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

        self.assertEqual(list(fibonacci(10)), expected)

    def test_generates_empty_sequence_for_zero_count(self) -> None:
        self.assertEqual(list(fibonacci(0)), [])

    def test_rejects_invalid_count(self) -> None:
        with self.assertRaises(TypeError):
            list(fibonacci(2.5))
        with self.assertRaises(ValueError):
            list(fibonacci(-1))


class DecoratorTests(unittest.TestCase):
    """Проверки декораторов."""

    def test_logs_function_call_and_preserves_result(self) -> None:
        @log_calls
        def multiply(left: int, right: int) -> int:
            return left * right

        with self.assertLogs("decorators", level="INFO") as captured:
            result = multiply(6, 7)

        self.assertEqual(result, 42)
        self.assertEqual(multiply.__name__, "multiply")
        self.assertIn("Вызов функции multiply", captured.output[0])
        self.assertIn("Функция multiply завершена", captured.output[1])

    def test_repeats_function_requested_number_of_times(self) -> None:
        calls = []

        @repeat(3)
        def record(value: int) -> int:
            calls.append(value)
            return value * 2

        self.assertEqual(record(5), [10, 10, 10])
        self.assertEqual(calls, [5, 5, 5])
        self.assertEqual(record.__name__, "record")

    def test_rejects_invalid_repeat_count(self) -> None:
        with self.assertRaises(TypeError):
            repeat(True)
        with self.assertRaises(ValueError):
            repeat(0)


class CsvProcessorTests(unittest.TestCase):
    """Проверки фильтрации и преобразования CSV."""

    def test_filters_and_transforms_student_results(self) -> None:
        expected = [
            StudentResult("Анна Иванова", 85),
            StudentResult("Виктор Сидоров", 73),
            StudentResult("Мария Смирнова", 100),
        ]

        self.assertEqual(successful_students(DATA_FILE), expected)

    def test_applies_custom_minimum_score(self) -> None:
        self.assertEqual(
            successful_students(DATA_FILE, minimum_score=90),
            [StudentResult("Мария Смирнова", 100)],
        )

    def test_rejects_invalid_minimum_score(self) -> None:
        with self.assertRaises(TypeError):
            successful_students(DATA_FILE, minimum_score=60.5)
        with self.assertRaises(ValueError):
            successful_students(DATA_FILE, minimum_score=101)

    def test_rejects_csv_without_required_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            csv_path = Path(temp_directory) / "students.csv"
            csv_path.write_text("student,result\nАнна,85\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                successful_students(csv_path)

    def test_rejects_invalid_score_in_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            csv_path = Path(temp_directory) / "students.csv"
            csv_path.write_text("name,score\nАнна,сто\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                successful_students(csv_path)


if __name__ == "__main__":
    unittest.main()
