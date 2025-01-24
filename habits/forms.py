from django import forms
from .models import Habit, Progress

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'goal']

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['count', 'completed']  # Include the 'completed' field
        widgets = {
            'count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }