from django.contrib import admin
from django.urls import include, path
from performance_review.views import FormAPIList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('review/', include('performance_review.urls')),
]
