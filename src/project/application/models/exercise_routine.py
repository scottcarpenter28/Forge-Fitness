import json
from typing import Dict, Any, List, Self

from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone

from application.enums.impact_options import ImpactOptions
from application.enums.routine_options import RoutineOptions
from application.forms.routine_form import RoutineForm
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

    def find_routine_exercises(self):
        return Exercise.objects.filter(routine=self).all()

    def __set_routine_exercises(self, routine_exercises: List[Dict[str, Any]]) -> None:
        """
        Deletes and then creates the exercises for the routine.
        :param routine_exercises: A list of exercises for the routine.
        :return: None
        """
        self.find_routine_exercises().delete()
        for i, exercise in enumerate(routine_exercises):
            Exercise.objects.create(
                routine=self,
                exercise=exercise.get("exercise"),
                reps=exercise.get("reps"),
                sets=exercise.get("sets"),
                duration=exercise.get("duration"),
                order=i,
            )

    def find_routine_equipment(self):
        return RoutineEquipment.objects.filter(routine=self).all()

    def __set_routine_equipment(self, routine_equipment: List[Equipment]) -> None:
        """
        Deletes and then creates the equipment for the routine.
        :param routine_equipment: A list of required equipments for the routine.
        :return: None
        """
        self.find_routine_equipment().delete()
        for equipment in routine_equipment:
            RoutineEquipment.objects.create(routine=self, equipment=equipment)

    def find_routine_target_muscles(self):
        return RoutineTargetMuscle.objects.filter(routine=self).all()

    def __set_routine_target_muscles(self, target_muscles: List[Muscle]) -> None:
        """
        Deletes and then creates the target muscles for the routine.
        :param target_muscles: A list of target muscles for the routine.
        :return: None.
        """
        self.find_routine_target_muscles().delete()
        for muscle in target_muscles:
            RoutineTargetMuscle.objects.create(routine=self, muscle=muscle)

    def find_routine_tags(self):
        return RoutineTag.objects.filter(routine=self).all()

    def __set_routine_tags(self, routine_tags: List[str]) -> None:
        """
        Deletes and then creates the tags for the routine.
        :param routine_tags:
        :return:
        """
        self.find_routine_tags().delete()
        for tag in routine_tags:
            RoutineTag.objects.create(routine=self, tag=tag)

    @classmethod
    def create_routine(cls, form: RoutineForm, user: User) -> Self:
        """
        Creates a new routine for the given form.
        :param form: The form containing the routine.
        :param user: The user who created the routine.
        :return: The new routine.
        """
        with transaction.atomic():
            routine = ExerciseRoutine.objects.create(
                creator=user,
                routine_name=form.cleaned_data["routine_name"],
                description=form.cleaned_data["description"],
                estimated_duration=form.cleaned_data["estimated_duration"],
                impact=form.cleaned_data["impact"],
                routine_type=form.cleaned_data["routine_type"],
                is_public=form.cleaned_data["is_public"],
                set_rest_time=form.cleaned_data["set_rest_time"],
                exercise_rest_time=form.cleaned_data["exercise_rest_time"],
            )
            routine.__set_routine_exercises(form.cleaned_data["routine"])
            routine.__set_routine_equipment(form.cleaned_data["equipment"])
            routine.__set_routine_target_muscles(form.cleaned_data["target_muscles"])
            routine.__set_routine_tags(form.cleaned_data["tags"])
            return routine

    def update_routine(self, form: RoutineForm) -> None:
        """
        Updates the routine with the new values.
        :param form: The form containing the updated routine.
        :return: None.
        """
        with transaction.atomic():
            self.routine_name = form.cleaned_data["routine_name"]
            self.description = form.cleaned_data["description"]
            self.estimated_duration = form.cleaned_data["estimated_duration"]
            self.set_rest_time = form.cleaned_data["set_rest_time"]
            self.updated_at = timezone.now()
            self.__set_routine_exercises(form.cleaned_data["routine"])
            self.__set_routine_equipment(form.cleaned_data["equipment"])
            self.__set_routine_target_muscles(form.cleaned_data["target_muscles"])
            self.__set_routine_tags(form.cleaned_data["tags"])
            self.save()

    def to_dict(self):
        exercises = [exercise.to_dict() for exercise in self.find_routine_exercises()]

        equipment_ids = [
            equipment.get_equipment_fk_id()
            for equipment in self.find_routine_equipment()
        ]

        target_muscle_ids = [
            muscle.get_muscle_fk_id() for muscle in self.find_routine_target_muscles()
        ]

        tags = ", ".join(tag.tag for tag in self.find_routine_tags())

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
