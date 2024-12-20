from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator)
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime



User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
         unique=True,
         max_length=50,
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
    name = models.CharField(max_length=200)
    slug = models.SlugField(
         unique=True,
         max_length=50,
         validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг категории содержит недопустимый символ'
        )]
    )

    class Meta:
            verbose_name = 'Категория'
            verbose_name_plural = 'Категории'
            default_related_name = 'categories'
            ordering = ['-name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения',max_length=256)
    year = models.PositiveIntegerField(
        verbose_name='Год выхода',
        validators=[
            MinValueValidator(
                0,
                message='Некоректное значение - год не может быть до н.э.'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message=(
                'Некоректное значение - вы указыаете еще не наступивший год'
            ))
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
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст отзыва')
    score = models.PositiveIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
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
        return f"Review: {self.title} - Score: {self.score} - Author: {self.author} - Text: {self.text[:20]}"


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
        return f"Comment by {self.author} on Review {self.review}: {self.text[:20]}..."
