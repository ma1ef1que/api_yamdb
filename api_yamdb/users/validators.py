import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Проверяет корректность username.
    """
    username_pattern = r'^[a-zA-Z][a-zA-Z0-9]{2,29}([._-]?[a-zA-Z0-9]+)*$'
    if not re.match(username_pattern, value):
        raise ValidationError(
            'Имя пользователя может содержать только латинские буквы, цифры, '
            'символы "-", "_" и ".", длиной от 3 до 30 символов.'
        )

    if 'me' in value.lower():
        raise ValidationError(
            'Имя пользователя не может содержать "me".'
        )

    return value
