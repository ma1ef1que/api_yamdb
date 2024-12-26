from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import (ConformationCodeSerializer, SignUpSerializer,
                          UserSerializer)
from .services import generate_confirmation_code, send_confirmation_email

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Представление пользователей сайта.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def get_me(self, request):
        user = request.user
        if request.method == 'GET':
            return Response(
                UserSerializer(user).data, status=status.HTTP_200_OK)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    """
    Регистрация пользователя и отправка кода подтверждения.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        user.confirmation_code = generate_confirmation_code(user)
        user.save()
        send_confirmation_email(user, email)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(APIView):
    """
    Получение JWT токена с использованием username и confirmation_code.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ConformationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if code == user.confirmation_code:
            token = str(RefreshToken.for_user(user).access_token)
            user.is_active = True
            user.save()
            return Response({'token': token}, status=status.HTTP_200_OK)

        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )

