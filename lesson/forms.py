from django import forms
from django.forms import ModelForm
from lesson.models import Lesson


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ('member', 'plan', 'date', 'hour', )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date',}),
            'hour': forms.NumberInput(attrs={'min': '0', 'max': '12', 'step': '1'}),
        }
