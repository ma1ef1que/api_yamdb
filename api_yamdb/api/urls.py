from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignUpView, TokenObtainView, UserViewSet
from .views import (
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

auth_urls = [
    path(
        'signup/', SignUpView.as_view(), name='sign_up'
    ),
    path(
        'token/', TokenObtainView.as_view(), name='get_token'
    )
]


urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router.urls)),
]
