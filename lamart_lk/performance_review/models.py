from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    team = models.ForeignKey('Team', on_delete=models.PROTECT, null=True, blank=True)
    birthday = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_team_leed = models.BooleanField(default=False)
    status_level = models.PositiveIntegerField(null=True, blank=True) 
    """чем больше число - тем меньшее место человек занивает в иерархии"""
    
    avatar_url = models.CharField(max_length=256, blank=True, null=True)
    def __str__(self):
        return self.first_name
    
    def get_full_name(self):
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.surname)
        return full_name.strip()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @receiver(user_signed_up)
    def populate_user(sociallogin, user,**kwargs):
        print(sociallogin.account.extra_data)
        user.birthday = sociallogin.account.extra_data['birthday']
        if sociallogin.account.extra_data['is_avatar_empty']:
            user.avatar_url = "https://avatars.yandex.net/get-yapic/" + sociallogin.account.extra_data['default_avatar_id'] + "/islands-retina-middle"
        user.gender = sociallogin.account.extra_data['sex']
        user.phone = sociallogin.account.extra_data['default_phone']
        user.save()

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
    leader_grade = models.IntegerField(null=True, blank=True) # лидерские качества
    feedback = models.IntegerField(null=True, blank=True) # работа с обратной свзязью, работа с информацией
    teamwork = models.IntegerField(null=True, blank=True) # организация командной работы, атмосфера в коллективе
    stress_resistance = models.IntegerField(null=True, blank=True) 

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