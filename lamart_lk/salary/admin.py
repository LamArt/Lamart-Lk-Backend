from django.contrib import admin

from salary.models import Role, Project, UsersProjects

admin.site.register(Role)
admin.site.register(Project)
admin.site.register(UsersProjects)
