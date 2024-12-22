from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


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
        max_length=150,
        blank=False,
        unique=True,
        null=False
    )
    email = models.EmailField(
        'e-mail',
        max_length=254,
        blank=False,
        unique=True,
        null=False
    )
    role = models.CharField(
        'Права пользователя',
        max_length=150,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=True,
        blank=True
    )
    bio = models.TextField('Расскажите о себе', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=16,
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
