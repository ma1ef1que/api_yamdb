import secrets

from django.core.mail import send_mail
from django.conf import settings


def generate_confirmation_code():
    """
    Генерирует случайный код подтверждения.
    """
    return secrets.token_urlsafe(16)


def send_confirmation_email(username, email, confirmation_code):
    """
    Отправляет письмо с кодом подтверждения на указанный email.
    """
    subject = 'Ваш код подтверждения'
    message = (
        f'Здравствуйте, {username}!\n\n'
        f'Вы запросили код подтверждения для регистрации на нашем сервисе.\n'
        f'Ваш код подтверждения: {confirmation_code}\n\n'
        f'Если вы не отправляли этот запрос, просто проигнорируйте это сообщение.'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
