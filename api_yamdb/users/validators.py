import re

from django.core.exceptions import ValidationError


def validate_username(value):
    '''
    Проверяет корректность username.
    '''
    if value == 'me':
        raise ValidationError('Имя пользователя не может содержать "me".')
    if not re.fullmatch(r'^[\w.@+-]+$', value):
        raise ValidationError(
            'Имя пользователя может содержать только латинские буквы, цифры, '
            'символы "-", "_" и "."'
        )
    return value
