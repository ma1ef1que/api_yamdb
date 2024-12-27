from django.contrib.auth.tokens import default_token_generator

from users.models import User


def generate_confirmation_code(user: User) -> str:
    """
    Генерирует случайный код подтверждения для пользователя.
    """
    return default_token_generator.make_token(user)
