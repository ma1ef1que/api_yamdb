from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Genre, Category, Title



class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('__all__')

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('__all__')

class TitleSerializer(serializers.ModelSerializer):

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

