from django import forms
from .models import *

class NewReview(forms.BaseModelForm):
    class Meta():
        model = Form
        fields = ['like', 'dislike', 'hard_skills', 'productivity', 'communication', 'initiative']
