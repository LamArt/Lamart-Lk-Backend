from django.db import models
from authentication.models import User


class Salary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(null=True, blank=True)
    last_salary_date = models.DateField(null=True, blank=True)
    credit = models.IntegerField(default=0)
    reward = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user}'

    @classmethod
    def get_salary_data(cls, user_instance):
        try:
            user_data = cls.objects.get(user=user_instance)
            return user_data
        except cls.DoesNotExist:
            return None
