from django.conf import settings
from django.db import models

class Form(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='created_forms', blank=False)
    about = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='forms_about', blank=False)
    like = models.TextField(verbose_name='Сильные стороны')
    dislike = models.TextField(verbose_name='Области роста')
    hard_skills = models.IntegerField()
    productivity = models.IntegerField()
    communication = models.IntegerField()
    initiative = models.IntegerField()

    # self review
    achievements = models.TextField(null=True, blank=True)
    ways_to_achieve = models.TextField(null=True, blank=True)

    # team leed 
    leader_skills = models.IntegerField(null=True, blank=True)
    feedback = models.IntegerField(null=True, blank=True)
    teamwork = models.IntegerField(null=True, blank=True)
    stress_resistance = models.IntegerField(null=True, blank=True) 

    # feedback
    feedback_date = models.DateField(null=True, blank=True)

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name