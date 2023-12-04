from django.conf import settings
from django.db import models


class TeamLeadFeedbackForm(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                   related_name='created_teamlead_forms', blank=False)
    about = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                 related_name='teamlead_forms_about',
                                 blank=False)
    feedback_date = models.DateField(null=True, blank=True)

    strengths = models.TextField(verbose_name='Сильные стороны')
    weaknesses = models.TextField(verbose_name='Области роста')
    hard_skills_rate = models.IntegerField()
    productivity_rate = models.IntegerField()
    communication_rate = models.IntegerField()
    initiative_rate = models.IntegerField()

    leader_skills = models.IntegerField(null=True)
    feedback_rate = models.IntegerField(null=True)
    teamwork_rate = models.IntegerField(null=True)
    stress_resistance_rate = models.IntegerField(null=True)

    manager_approve = models.BooleanField(default=False)


class EmployeeFeedbackForm(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                   related_name='created_employee_forms', blank=False)
    about = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                  related_name='employee_forms_about',
                                  blank=False)
    team = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee_team", blank=False)

    feedback_date = models.DateField(null=True, blank=True)

    achievements = models.TextField(null=True, blank=True)
    ways_to_achieve = models.TextField(null=True, blank=True)

    strengths = models.TextField(verbose_name='Сильные стороны')
    weaknesses = models.TextField(verbose_name='Области роста')
    hard_skills_rate = models.IntegerField()
    productivity_rate = models.IntegerField()
    communication_rate = models.IntegerField()
    initiative_rate = models.IntegerField()


class Team(models.Model):
    name = models.CharField(max_length=50)
    team_lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_lead',
                                  blank=False)

    def __str__(self):
        return self.name