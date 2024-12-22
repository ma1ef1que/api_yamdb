from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс настройки раздела произведений."""

    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name', 'year', 'category')


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'genre',
        'title'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('genre',)
    search_fields = ('title',)
