from django.db import models
from authentication.models import User


class Role(models.Model):
    name = models.CharField(max_length=50)
    salary_formula = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    jira_key = models.CharField(max_length=20)
    members = models.ManyToManyField(User, through='UsersProjects')
    rate = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


class UsersProjects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    credit = models.PositiveIntegerField(null=True, blank=True)
    reward = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.role.name} - {self.project.name}"
