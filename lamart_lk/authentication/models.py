from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=False)
    surname = models.CharField(max_length=50, null=True, blank=True)
    teams = models.ManyToManyField('Team', related_name='members', blank=True)
    birthday = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    status_level = models.PositiveIntegerField(null=True, blank=True)
    """чем больше число - тем меньшее место человек занивает в иерархии"""

    avatar_url = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = "%s %s %s" % (self.last_name, self.first_name, self.surname)
        return full_name.strip()


class ProviderToken(models.Model):
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=512, null=True, blank=True)
    expires_in = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_tokens')
    provider = models.CharField(max_length=64)
    organisation = models.CharField(max_length=256)
    user_provider_email = models.EmailField(blank=False, unique=False)

    def __str__(self):
        return f'{self.user} - {self.provider} provider'


class Team(models.Model):
    name = models.CharField(max_length=50)
    jira_key = models.CharField(max_length=20)
    rate = models.PositiveIntegerField(null=False, blank=False)
    team_lead = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_lead_in',
                                  blank=False, null=True)

    def __str__(self):
        return self.name
