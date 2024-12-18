from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Genre, Category, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (GenreSerializer, TitleSerializer, CategorySerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (filters.DjangoFilterBackend, )
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_fields = ('category', 'genre', 'name', 'year')


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class CommentViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]

