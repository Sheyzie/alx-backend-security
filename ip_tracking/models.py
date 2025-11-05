from django.db import models


class RequestLog(models.Model):
    ip_address = models.IPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    path = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.timestamp}-{self.ip_address}-{self.path}'


class BlockedIP(models.Model):
    ip_address = models.IPAddressField()

    def __str__(self):
        return self.ip_address
    

class SuspiciousIP(models.Model):
    ip_address = models.IPAddressField()
    path = models.TextField()
    reason = models.CharField(max_length=255)
    flagged_at = models.DateTimeField(auto_now_add=True)
