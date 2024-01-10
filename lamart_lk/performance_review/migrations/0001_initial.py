# Generated by Django 4.2.3 on 2024-01-10 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamLeadFeedbackForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_date', models.DateField(blank=True, null=True)),
                ('strengths', models.TextField(verbose_name='Сильные стороны')),
                ('weaknesses', models.TextField(verbose_name='Области роста')),
                ('hard_skills_rate', models.IntegerField()),
                ('productivity_rate', models.IntegerField()),
                ('communication_rate', models.IntegerField()),
                ('initiative_rate', models.IntegerField()),
                ('leader_skills', models.IntegerField(null=True)),
                ('feedback_rate', models.IntegerField(null=True)),
                ('teamwork_rate', models.IntegerField(null=True)),
                ('stress_resistance_rate', models.IntegerField(null=True)),
                ('manager_approve', models.BooleanField(default=False)),
                ('about', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='teamlead_forms_about', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                 related_name='created_teamlead_forms', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='employee_team_for_teamlead', to='authentication.team')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeFeedbackForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_date', models.DateField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
                ('ways_to_achieve', models.TextField(blank=True, null=True)),
                ('strengths', models.TextField(verbose_name='Сильные стороны')),
                ('weaknesses', models.TextField(verbose_name='Области роста')),
                ('hard_skills_rate', models.IntegerField()),
                ('productivity_rate', models.IntegerField()),
                ('communication_rate', models.IntegerField()),
                ('initiative_rate', models.IntegerField()),
                ('about', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='employee_forms_about', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                 related_name='created_employee_forms', to=settings.AUTH_USER_MODEL)),
                ('team',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_team_employee',
                                   to='authentication.team')),
            ],
        ),
    ]
