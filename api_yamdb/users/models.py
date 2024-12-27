from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username
from api_yamdb.settings import USER_INFO_MAX_LENGTH, MAX_LENGTH_CONF_CODE


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        ('admin', ADMIN),
        ('moderator', MODERATOR),
        ('user', USER)
    ]
    username = models.CharField(
        'Имя пользователя',
        validators=(validate_username,),
        max_length=USER_INFO_MAX_LENGTH,
        blank=False,
        unique=True,
        null=False
    )
    email = models.EmailField(
        'e-mail',
        max_length=USER_INFO_MAX_LENGTH,
        blank=False,
        unique=True,
        null=False
    )
    role = models.CharField(
        'Права пользователя',
        max_length=USER_INFO_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=USER_INFO_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=USER_INFO_MAX_LENGTH,
        blank=True
    )
    bio = models.TextField('Расскажите о себе', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=MAX_LENGTH_CONF_CODE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email', '-date_joined',)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
