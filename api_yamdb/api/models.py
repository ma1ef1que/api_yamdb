from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения',max_length=200)
    year = models.IntegerField('Год выхода')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre', related_name='titles', verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='titles', verbose_name='Категория')

    def __str__(self):
        return self.name
    

class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


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
