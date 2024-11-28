from datetime import datetime


class ValidationError(Exception):
    pass


def validate_date(date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Неверный формат даты. Используйте формат YYYY-MM-DD.")


def validate_priority(priority: str):
    if priority not in ["низкий", "средний", "высокий"]:
        raise ValidationError("Недопустимый приоритет. Выберите из: низкий, средний, высокий.")


def validate_non_empty(value: str, field_name: str):
    if not value.strip():
        raise ValidationError(f"Поле '{field_name}' не может быть пустым.")