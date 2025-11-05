from ratelimit.decorators import ratelimit
# from django.utils.decorators import method_decorator
from django.http import JsonResponse

# Function-based view version
@ratelimit(key='user', rate='10/m', method='GET', block=True)
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def api_view(request):
    return JsonResponse({'message': 'OK'})
