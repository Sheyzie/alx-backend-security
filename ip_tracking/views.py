from django_ratelimit.decorators import ratelimit
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
# from django.utils.decorators import method_decorator
from django.http import JsonResponse


User = get_user_model()

# Function-based view version
@ratelimit(key='user', rate='10/m', method='GET', block=True)
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def api_view(request):
    return JsonResponse({'message': 'OK'})


# register user view
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create auth token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "user": serializer.data,
                "token": token.key
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )