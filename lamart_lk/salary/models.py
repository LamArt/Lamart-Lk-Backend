from django.db import models
from authentication.models import User, Team


class Role(models.Model):
    name = models.CharField(max_length=50)
    salary_formula = models.TextField(blank=False, null=False)
    is_team_lead = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    credit = models.PositiveIntegerField(null=True, blank=True)
    reward = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.team.name} - {self.user} -  {self.role.name}"
