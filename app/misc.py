import os


def get_environ(key: str) -> str:
    """Возвращает переменную окружения, либо вызывает ошибку ValueError"""
    value = os.getenv(key, None)
    if value is None:
        raise ValueError(f"Укажите переменную окружения: {key}")
    return value
