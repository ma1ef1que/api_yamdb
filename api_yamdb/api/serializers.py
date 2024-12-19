from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Genre, Category, Title, Review, Comment


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('__all__')

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('__all__')

class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    class Meta:
        read_only_fields = ('rating', )
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        
        model = Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(limit_value=0),
            MaxValueValidator(limit_value=10)
        ]
    )

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review',)
