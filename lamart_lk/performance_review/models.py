from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):
    # title = models.CharField(verbose_name='name', max_length=32)

    like = models.TextField(verbose_name='Сильные стороны', null=False)
    dislike = models.TextField(verbose_name='Области роста', null=False)

    hard_skills = models.IntegerField(verbose_name='hard skill') # отрпавлять по ползунку
    productivity = models.IntegerField(verbose_name='productivity') # отрпавлять по ползунку
    communication = models.IntegerField(verbose_name='communication') # отрпавлять по ползунку
    initiative = models.IntegerField(verbose_name='initiative2') # отрпавлять по ползунку

    # self review
    achievements = models.TextField(null=True)
    ways_to_achieve = models.TextField(null=True)

    # team leed 
    team_leed_grade = models.IntegerField(null=True) # отрпавлять по ползунку
    feedback_date = models.DateField(null=True)
    # def __str__(self):
    #     return self.title
    # class Meta:
    #     verbose_name = 'Form'
    #     verbose_name_plural = 'Forms'

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Emploee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    is_team_leed = models.BooleanField(default=False)
    status_level = models.PositiveIntegerField() # чем больше число - тем меньшее место человек занивает в иерархии

    def __str__(self):
        return User.first_name

class Project(models.Model):
    name = models.CharField(max_length=70)
    discription = models.TextField()
    is_complited = models.BooleanField(default=True)
    members = models.ManyToManyField(Emploee, related_name='projects')

    def __str__(self):
        return self.name