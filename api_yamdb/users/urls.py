from django.urls import path

from api.views import SignUpView, TokenObtainView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('token/', TokenObtainView.as_view(), name='get_token')
]
