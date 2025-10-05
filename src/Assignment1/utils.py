"""Utility functions"""


def calculate_average(numbers: list[float]) -> float:
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def format_percentage(value: float, total: float) -> str:
    if total == 0:
        return "0%"
    return f"{(value / total) * 100:.1f}%"
