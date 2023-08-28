from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=False)
    surname = models.CharField(max_length=50, null=True, blank=True)
    team = models.ForeignKey('Team', on_delete=models.PROTECT, null=True, blank=True)
    birthday = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_team_lead = models.BooleanField(default=False)
    status_level = models.PositiveIntegerField(null=True, blank=True)
    """чем больше число - тем меньшее место человек занивает в иерархии"""
    
    avatar_url = models.CharField(max_length=256, blank=True, null=True)
    def __str__(self):
        return self.first_name
    
    def get_full_name(self):
        full_name = "%s %s %s" % (self.last_name, self.first_name, self.surname)
        return full_name.strip()
    

class Form(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='created_forms', blank=False)
    about = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='forms_about', blank=False)
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
    

# class Project(models.Model):
#     name = models.CharField(max_length=70)
#     discription = models.TextField()
#     is_complited = models.BooleanField(default=True)
#     members = models.ManyToManyField(User, related_name='projects', null=True)

#     def __str__(self):
#         return self.name