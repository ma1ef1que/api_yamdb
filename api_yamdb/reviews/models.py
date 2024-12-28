from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinValueValidator, RegexValidator)
from django.db import models

from api_yamdb.settings import (
    NAME_LENGTH,
    SLUG_LENGTH,
    MIN_SCORE_VALIDATOR,
    STR_TEXT_LENGTH,
    MAX_SCORE_VALIDATOR,
    MIN_YEAR_VALIDATOR
)


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_LENGTH,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг категории содержит недопустимый символ'
        )]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_LENGTH,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Слаг категории содержит недопустимый символ'
            )
        ]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'
        ordering = ['-name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=NAME_LENGTH,
        validators=[MaxLengthValidator(NAME_LENGTH)]
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выхода',
        validators=[
            MinValueValidator(
                MIN_YEAR_VALIDATOR,
                message='Некорректное значение - год не может быть до н.э.'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message=(
                    'Некорректное значение - вы указыаете еще '
                    'не наступивший год'
                )
            )
        ],
        db_index=True
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Жанры и произведения'
        verbose_name_plural = 'Таблица жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(MIN_SCORE_VALIDATOR),
            MaxValueValidator(MAX_SCORE_VALIDATOR),
        ]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            )
        ]

    def __str__(self):
        return (
            f'Review: {self.title} - Score: {self.score} - '
            f'Author: {self.author} - Text: {self.text[:STR_TEXT_LENGTH]}'
        )


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ['-pub_date']

    def __str__(self):
        return (
            f'Comment by {self.author} on Review '
            f'{self.review}: {self.text[:STR_TEXT_LENGTH]}...'
        )
