from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    surname = models.CharField(max_length=50) # отчество
    team = models.ForeignKey('Team', on_delete=models.PROTECT, null=True)
    is_team_leed = models.BooleanField(default=False)
    status_level = models.PositiveIntegerField(null=True) # чем больше число - тем меньшее место человек занивает в иерархии

    def __str__(self):
        return self.first_name
    
    def get_full_name(self):
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.surname)
        return full_name.strip()

class Form(models.Model):
    like = models.TextField(verbose_name='Сильные стороны', null=False)
    dislike = models.TextField(verbose_name='Области роста', null=False)

    hard_skills = models.IntegerField() # отрпавлять по ползунку
    productivity = models.IntegerField() # отрпавлять по ползунку
    communication = models.IntegerField() # отрпавлять по ползунку
    initiative = models.IntegerField() # отрпавлять по ползунку

    # self review
    achievements = models.TextField(null=True)
    ways_to_achieve = models.TextField(null=True)

    # team leed 
    team_leed_grade = models.IntegerField(null=True) # отрпавлять по ползунку
    feedback_date = models.DateField(null=True)

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    name = models.CharField(max_length=70)
    discription = models.TextField()
    is_complited = models.BooleanField(default=True)
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name