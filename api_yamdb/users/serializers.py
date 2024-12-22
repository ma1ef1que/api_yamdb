from django.contrib.auth import get_user_model
from django.forms import ValidationError
from rest_framework import serializers


from .validators import validate_username


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ConformationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_username]
    )
    email = serializers.EmailField(max_length=254, required=True,)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            return data
        elif User.objects.filter(username=username).exists():
            raise ValidationError(
                'Пользователь с таким именем уже зарегистрирован.'
            )
        elif User.objects.filter(email=email).exists():
            raise ValidationError(
                'Такой e-mail уже зарегистрирован.'
            )
        return data
