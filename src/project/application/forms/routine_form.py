from django import forms
from django.core.validators import MinValueValidator

from application.enums.impact_options import ImpactOptions
from application.enums.routine_options import RoutineOptions
from application.models import Equipment, Muscle


class RoutineForm(forms.Form):
    routine_name = forms.CharField(
        required=True, error_messages={"required": "Routine name is required."}
    )
    description = forms.CharField(
        required=True,
        max_length=250,
        error_messages={"required": "Description is required."},
        widget=forms.Textarea,
    )
    estimated_duration = forms.IntegerField(
        required=True,
        error_messages={
            "required": "Estimated time is required.",
            "min_value": "Estimated time must at least 5 minutes.",
        },
        validators=[MinValueValidator(4)],
    )
    set_rest_time = forms.IntegerField(
        initial=45,
        help_text="Rest time between sets in seconds.",
        error_messages={
            "required": "Rest time between sets is required.",
            "min_value": "Set rest time must at least 5 seconds.",
        },
        validators=[MinValueValidator(4)],
    )
    exercise_rest_time = forms.IntegerField(
        initial=60,
        help_text="Rest time between exercise in seconds.",
        error_messages={
            "required": "Rest time between exercises is required.",
            "min_value": "Rest time must at least 5 seconds.",
        },
        validators=[MinValueValidator(4)],
    )
    impact = forms.ChoiceField(
        initial=ImpactOptions.MEDIUM,
        required=True,
        choices=ImpactOptions.choices,
        error_messages={"required": "Impact level is required."},
    )
    tags = forms.CharField(required=False, help_text="Comma separated tags")
    target_muscles = forms.ModelMultipleChoiceField(
        queryset=Muscle.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        error_messages={
            "required": "At least one target muscle is required.",
            "invalid": "The muscle group selected is not valid.",
        },
    )
    routine_type = forms.ChoiceField(
        initial=RoutineOptions.CARDIO,
        required=True,
        choices=RoutineOptions.choices,
        error_messages={"required": "Routine type is required."},
    )
    equipment = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Equipment.objects.all(),
        widget=forms.SelectMultiple,
        error_messages={"invalid": "The equipment selected is not valid."},
    )
    is_public = forms.BooleanField(
        initial=False, required=False, widget=forms.CheckboxInput
    )
    routine = forms.JSONField(
        initial=[],
        required=True,
        error_messages={"required": "Your routine is empty. Build your routine."},
    )

    def clean_tags(self):
        tags = self.cleaned_data["tags"]
        if tags:
            return [tag.strip().replace(" ", "_") for tag in tags.split(",")]
