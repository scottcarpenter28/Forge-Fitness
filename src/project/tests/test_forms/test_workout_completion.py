import uuid

from django.test import TestCase

from application.forms.workout_completion import WorkoutCompletionForm


class TestWorkoutCompletionForm(TestCase):

    def setUp(self):
        self.form_data = {
            "workout_uid": uuid.uuid4(),
            "workout_start": "2025-03-12T22:44:29.803Z",
            "workout_end": "2025-03-12T22:44:29.803Z",
            "completion_status": "Completed",
        }

    def test_normal_workout_completion(self):
        form = WorkoutCompletionForm(self.form_data)
        self.assertTrue(form.is_valid())
