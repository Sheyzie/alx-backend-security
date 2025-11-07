from django.urls import path
from rest_framework.authtoken import views
from .views import RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('api-token-auth/', views.obtain_auth_token),
]