from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls.base import reverse

from application.models import (
    ExerciseRoutine,
    Exercise,
    Equipment,
    Muscle,
    RoutineTag,
    RoutineTargetMuscle,
    RoutineEquipment,
)


class TestAccountCreationView(TestCase):
    def setUp(self):
        m1 = Muscle(muscle_name="Abs")
        m2 = Muscle(muscle_name="Chest")
        m1.save()
        m2.save()

        e1 = Equipment(equipment_name="Mat")
        e2 = Equipment(equipment_name="Dumbbell")
        e1.save()
        e2.save()

        self.form_data = {
            "routine_name": "Test Routine",
            "description": "This is a test routine description",
            "estimated_duration": 10,
            "impact": "Low",
            "tags": "example, tag, new routine",
            "target_muscles": [m1.id, m2.id],
            "routine_type": "Cardio",
            "equipment": [e1.id, e2.id],
            "is_public": True,
            "set_rest_time": 45,
            "exercise_rest_time": 60,
            "routine": '[{"id": "exercise_0", "exercise": "Test 1", "reps": 10, "sets": 3, "duration": 30}, {"id": "exercise_1", "exercise": "Test 2", "reps": 10, "sets": 3, "duration": 30}]',
        }

        self.client = Client()
        User.objects.create_user("test", "test@email.com", "password")
        self.client.login(username="test", password="password")

    def tearDown(self):
        self.client.logout()

    def test_form_success(self):
        response = self.client.post(reverse("create_routine"), self.form_data)
        messages = list(get_messages(response.wsgi_request))
        assert str(messages[0]) == "Routine created successfully!"

        routine = ExerciseRoutine.objects.first()
        assert routine.routine_name == "Test Routine"

        assert len(Exercise.objects.filter(routine=routine).all()) == 2
        assert len(RoutineEquipment.objects.filter(routine=routine).all()) == 2
        assert len(RoutineTargetMuscle.objects.filter(routine=routine).all()) == 2

        routine_tags = RoutineTag.objects.filter(routine=routine).all()
        assert len(RoutineTag.objects.filter(routine=routine)) == 3
        assert routine_tags[1].tag == "tag"
        assert routine_tags[2].tag == "new_routine"
