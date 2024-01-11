from django.conf import settings
from django.db import models
from salary.models import Team


class PerformanceReview(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performance_review')
    created_at = models.DateTimeField(auto_now_add=True)
    stage = models.IntegerField(default=1)

class TeamLeadFeedbackForm(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                   related_name='created_teamlead_forms', blank=False)
    about = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                              related_name='teamlead_forms_about',
                              blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="employee_team_for_teamlead",
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
    performance_review = models.ForeignKey(PerformanceReview, null=True, on_delete=models.CASCADE, related_name="teamlead_form")


class EmployeeFeedbackForm(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                   related_name='created_employee_forms', blank=False)
    about = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                              related_name='employee_forms_about',
                              blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="employee_team_employee",
                             blank=False)

    feedback_date = models.DateField(null=True, blank=True)

    achievements = models.TextField(null=True, blank=True)
    ways_to_achieve = models.TextField(null=True, blank=True)

    strengths = models.TextField(verbose_name='Сильные стороны')
    weaknesses = models.TextField(verbose_name='Области роста')
    hard_skills_rate = models.IntegerField()
    productivity_rate = models.IntegerField()
    communication_rate = models.IntegerField()
    initiative_rate = models.IntegerField()
    performance_review = models.ForeignKey(PerformanceReview, null=True, on_delete=models.CASCADE, related_name="employee_form")
