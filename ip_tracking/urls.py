from django.urls import path
from rest_framework.authtoken import views
from .views import RegisterView, api_view


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-view/', api_view, name='api-view'),
]