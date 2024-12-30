from django import forms

from application.enums.impact_options import ImpactOptions
from application.enums.routine_options import RoutineOptions
from application.models import Equipment, Muscle


class RoutineForm(forms.Form):
    routine_name = forms.CharField()
    description = forms.CharField()
    estimated_time = forms.IntegerField()
    impact = forms.ChoiceField(choices=ImpactOptions.choices)
    tags = forms.CharField()
    target_muscles = forms.ModelChoiceField(
        queryset=Muscle.objects.all(), empty_label="", widget=forms.SelectMultiple
    )
    routine_type = forms.ChoiceField(choices=RoutineOptions.choices)
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(), empty_label="", widget=forms.SelectMultiple
    )
    routine = forms.JSONField()
