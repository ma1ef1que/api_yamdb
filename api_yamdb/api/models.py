from django.db import models


class Rating(models.Model):
    pass


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
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='titles', verbose_name='Рейтинг')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre', related_name='titles', verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='titles', verbose_name='Категория')

    def __str__(self):
        return self.name
    

class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Comment(models.Model):
    pass


class Review(models.Model):
    pass


