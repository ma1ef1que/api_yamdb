import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Проверяет корректность username.
    """
    if len(value) > 30:
        raise ValidationError(
            'Имя пользователя не может быть длиннее 30 символов.'
        )

    username_pattern = r'^[a-zA-Z][a-zA-Z0-9._-]{2,29}$'
    if not re.match(username_pattern, value):
        raise ValidationError(
            'Имя пользователя может содержать только латинские буквы, цифры, '
            'символы "-", "_" и ".", длиной от 3 до 30 символов.'
        )

    if 'me' == value.lower():
        raise ValidationError(
            'Имя пользователя не может содержать "me".'
        )

    return value


def validate_email(value):
    """
    Проверяет корректность email.
    """
    if len(value) > 254:
        raise ValidationError(
            'Адрес электронной почты не может быть длиннее 254 символов.'
        )
    return value
