from django import forms

from application.enums.workout_completion_status import WorkoutCompletionStatus


class WorkoutCompletionForm(forms.Form):
    workout_uid = forms.UUIDField(required=True)
    workout_start = forms.DateTimeField(required=True)
    workout_end = forms.DateTimeField(required=True)
    completion_status = forms.ChoiceField(choices=WorkoutCompletionStatus.choices)
