from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from application.models.completed_routine import CompletedRoutine


class TestCompletedRoutinesModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("test", "test@email.com", "password")

    def test_create_completed_routine(self):
        now = datetime.now(tz=timezone.utc)
        cr = CompletedRoutine(
            user=self.user,
            routine=None,
            start_time=now - timedelta(minutes=20),
            end_time=now,
        )
        cr.save()
        assert cr.routine_duration == "20:00"
