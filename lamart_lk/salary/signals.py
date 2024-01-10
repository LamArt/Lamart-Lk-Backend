from django.db.models.signals import post_save
from django.dispatch import receiver
from salary.models import TeamMember


@receiver(post_save, sender=TeamMember)
def add_user_to_team(instance, **kwargs):
    if kwargs.get('created', False):
        instance.user.teams.add(instance.team)
