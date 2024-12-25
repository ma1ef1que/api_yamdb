from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('token/', views.TokenObtainView.as_view(), name='get_token')
]
