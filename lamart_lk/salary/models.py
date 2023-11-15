from django.db import models
from authentication.models import User

class Salary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(null=True, blank=True)
    last_salary_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user}, Ставка: {self.rate}'
