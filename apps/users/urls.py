from django.urls import path
from .views import LoginView, RegisterView, ProfileView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='user-register'),
    path('auth/login/',    LoginView.as_view(),    name='user-login'),
    path('auth/me/',       ProfileView.as_view(),  name='user-profile'),
]