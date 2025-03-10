from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from application.models.exercise_routine import Exercise


class CompletedRoutine(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)
    routine_name = models.CharField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def routine_duration(self):
        minutes = self.end_time.minute - self.start_time.minute
        seconds = self.end_time.second - self.end_time.second
        return f"{minutes:02}:{seconds:02}"
