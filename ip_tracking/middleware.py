from django.http import JsonResponse
import logging
# from django_ip_geolocation.decorators import with_ip_geolocation
from django.core.cache import cache

from .models import RequestLog, BlockedIP


# Basic configuration (optional, but good for simple cases)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get a logger instance
logger = logging.getLogger(__name__)

# Get IP from request
def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')

    if xff:
        # should return string value like '203.0.113.195, 70.41.3.18, 150.172.238.178'
        # the first set is the real client ip
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

# get ip_address location addeded by django_ip_geolocation middleware
def get_location(request):
    # get the location object
    location = request.geolocation

    # cache result for 1hour
    cache.set('location', location, timeout=60 * 60 * 24)
    
    return location

class LogRequestDetail:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # get request details
        ip_address = get_client_ip(request)
        method = request.method
        path = request.path
        params = request.GET
        headers_dict = {k: v for k, v in request.META.items() if k.startswith('HTTP_')}
        body = request.body

        location = get_location(request)

        country = location.get('country_name')
        city = location.get('city')

        # check if ip is blocked
        is_blocked = BlockedIP.objects.filter(ip_address=ip_address).exists()

        if is_blocked:
            return JsonResponse('403 Forbidden')

        request_log, created = RequestLog.objects.get_or_create(path=path, ip_address=ip_address, country=country, city=city)

        response = self.get_response(request)

        return response