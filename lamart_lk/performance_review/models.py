from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


class User(AbstractUser):
    surname = models.CharField(max_length=50, null=True)
    team = models.ForeignKey('Team', on_delete=models.PROTECT, null=True)
    birthday = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=12, null=True)
    gender = models.CharField(max_length=10, null=True)
    is_team_leed = models.BooleanField(default=False)
    status_level = models.PositiveIntegerField(null=True) # чем больше число - тем меньшее место человек занивает в иерархии

    def __str__(self):
        return self.first_name
    
    def get_full_name(self):
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.surname)
        return full_name.strip()

class Form(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='created_forms')
    about = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='forms_about')
    like = models.TextField(verbose_name='Сильные стороны')
    dislike = models.TextField(verbose_name='Области роста')
    hard_skills = models.IntegerField()
    productivity = models.IntegerField()
    communication = models.IntegerField()
    initiative = models.IntegerField()

    # self review
    achievements = models.TextField(null=True)
    ways_to_achieve = models.TextField(null=True)

    # team leed 
    leader_grade = models.IntegerField(null=True) # лидерские качества
    feedback = models.IntegerField(null=True) # работа с обратной свзязью, работа с информацией
    teamwork = models.IntegerField(null=True) # организация командной работы, атмосфера в коллективе
    stress_resistance = models.IntegerField(null=True) 

    feedback_date = models.DateField(null=True)

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    user_data = user.socialaccount_set.filter(provider='yandex')[0].extra_data
    user.profile.avatar_url = "https://avatars.yandex.net/get-yapic/" + user_data['avatar_id'] + "/islands-retina-middle"
    user.profile.gender = user_data['sex']
    user.profile.birthday = user_data['birthday']
    user.profile.save()


""" class Project(models.Model):
    name = models.CharField(max_length=70)
    discription = models.TextField()
    is_complited = models.BooleanField(default=True)
    members = models.ManyToManyField(User, related_name='projects', null=True)

    def __str__(self):
        return self.name """