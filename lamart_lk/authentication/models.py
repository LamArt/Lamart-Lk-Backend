from django.db import models
from performance_review.models import User

class ProviderToken(models.Model):
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=512)
    expires_in = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_tokens')
    provider = models.CharField(max_length=64)