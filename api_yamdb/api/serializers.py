from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username
from api_yamdb.settings import (
    MIN_SCORE_VALIDATOR,
    MAX_SCORE_VALIDATOR,
    USER_INFO_MAX_LENGTH
)
from .utils import generate_confirmation_code


User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class TitleGETSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(limit_value=MIN_SCORE_VALIDATOR),
            MaxValueValidator(limit_value=MAX_SCORE_VALIDATOR)
        ]
    )
    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(), required=False
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title = self.context['title']

        if (self.instance is None
                and title.reviews.filter(author=author).exists()):
            raise ValidationError('Вы уже оставили отзыв на это произведение.')

        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USER_INFO_MAX_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'}
            )

        return data

    def save(self):
        username = self.validated_data['username']
        user = get_object_or_404(User, username=username)
        user.is_active = True
        user.save()

        token = str(RefreshToken.for_user(user).access_token)
        return {'token': token}


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USER_INFO_MAX_LENGTH,
        required=True,
        validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=USER_INFO_MAX_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, **kwargs):
        email = self.validated_data['email']
        username = self.validated_data['username']

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        if not created:
            user.confirmation_code = generate_confirmation_code(user)
            user.save()

        self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user):
        confirmation_message = (
            f'Здравствуйте!\n\n'
            f'Вы запросили код подтверждения для регистрации на сервисе.\n'
            f'Ваш код подтверждения: {user.confirmation_code}\n\n'
            f'Если вы не отправляли этот запрос, '
            f'просто проигнорируйте это сообщение.'
        )
        send_mail(
            subject='Код подтверждения',
            message=confirmation_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                {
                    'username': (
                        'Пользователь с таким '
                        'именем уже зарегистрирован.'
                    )
                }
            )
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                {
                    'email': (
                        'Такой e-mail '
                        'уже зарегистрирован.'
                    )
                }
            )
        return data
