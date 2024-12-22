from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from .models import User


def generate_confirmation_code(user: User) -> str:
    """
    Генерирует случайный код подтверждения для пользователя.
    """
    return default_token_generator.make_token(user)


def send_confirmation_email(user: User, email: str) -> None:
    """
    Отправляет письмо с кодом подтверждения на указанный email.
    """
    confirmation_message = (
        f'Здравствуйте!\n\n'
        f'Вы запросили код подтверждения для регистрации на нашем сервисе.\n'
        f'Ваш код подтверждения: {user.confirmation_code}\n\n'
        f'Если вы не отправляли этот запрос, '
        f'просто проигнорируйте это сообщение.'
    )
    send_mail(
        subject='Код подтверждения',
        message=confirmation_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
