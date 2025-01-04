import json

from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from application.enums.impact_options import ImpactOptions
from application.enums.routine_options import RoutineOptions
from .muscles import Muscle
from .equipment import Equipment


class ExerciseRoutine(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    routine_name = models.CharField(max_length=255)
    description = models.TextField()
    estimated_duration = models.IntegerField(
        help_text="Estimated time the routine takes in minutes."
    )
    impact = models.CharField(
        choices=ImpactOptions.choices,
        help_text="The difficulty of the exercise routine.",
    )
    routine_type = models.CharField(
        choices=RoutineOptions.choices, max_length=255, help_text="Type of routine."
    )
    is_public = models.BooleanField(
        default=False, help_text="Flag determining if this routine is public."
    )
    set_rest_time = models.IntegerField(
        default=45, help_text="Amount of rest between sets in seconds."
    )
    exercise_rest_time = models.IntegerField(
        default=600, help_text="Amount of rest between exercises in seconds."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        routine_exercises = Exercise.objects.filter(routine=self).all()
        exercises = [exercise.to_dict() for exercise in routine_exercises]

        routine_equipment = RoutineEquipment.objects.filter(routine=self).all()
        equipment_ids = [
            equipment.get_equipment_fk_id() for equipment in routine_equipment
        ]

        routine_target_muscles = RoutineTargetMuscle.objects.filter(routine=self).all()
        target_muscle_ids = [
            muscle.get_muscle_fk_id() for muscle in routine_target_muscles
        ]

        routine_tags = RoutineTag.objects.filter(routine=self).all()
        tags = ", ".join(tag.tag for tag in routine_tags)

        return {
            "routine_name": self.routine_name,
            "description": self.description,
            "estimated_duration": self.estimated_duration,
            "impact": self.impact,
            "tags": tags,
            "target_muscles": target_muscle_ids,
            "routine_type": "Cardio",
            "equipment": equipment_ids,
            "is_public": self.is_public,
            "set_rest_time": self.set_rest_time,
            "exercise_rest_time": self.exercise_rest_time,
            "routine": json.dumps(exercises),
        }


class Exercise(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    routine = models.ForeignKey(ExerciseRoutine, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=255, help_text="The name of the exercise.")
    reps = models.IntegerField(default=10, help_text="Number of reps (Strength only).")
    sets = models.IntegerField(default=3, help_text="Number of sets (Strength only).")
    duration = models.IntegerField(
        default=30, help_text="Duration of the exercise in seconds (Cardio only)."
    )
    order = models.IntegerField(
        help_text="The order of the exercise within the routine."
    )

    def to_dict(self):
        return {
            "exercise": self.exercise,
            "reps": self.reps,
            "sets": self.sets,
            "duration": self.duration,
        }


class RoutineTag(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    routine = models.ForeignKey(ExerciseRoutine, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255)


class RoutineTargetMuscle(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    routine = models.ForeignKey(ExerciseRoutine, on_delete=models.CASCADE)
    muscle = models.ForeignKey(Muscle, on_delete=models.CASCADE)

    def get_muscle_fk_id(self) -> int:
        return self.muscle.id


class RoutineEquipment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    routine = models.ForeignKey(ExerciseRoutine, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def get_equipment_fk_id(self) -> int:
        return self.equipment.id
