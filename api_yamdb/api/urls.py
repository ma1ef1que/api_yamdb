from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='posts')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
]
