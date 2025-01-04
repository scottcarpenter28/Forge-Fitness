import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls.base import reverse

from application.forms.routine_form import RoutineForm
from application.utils.form_messages import add_error_messages
from application.models.exercise_routine import (
    ExerciseRoutine,
    Exercise,
    RoutineTag,
    RoutineTargetMuscle,
    RoutineEquipment,
)


@login_required
def create_routine(request):
    form = RoutineForm()
    if request.method == "POST":
        form = RoutineForm(request.POST)
        if form.is_valid():
            try:
                routine = ExerciseRoutine.objects.create(
                    creator=request.user,
                    routine_name=form.cleaned_data["routine_name"],
                    description=form.cleaned_data["description"],
                    estimated_duration=form.cleaned_data["estimated_duration"],
                    impact=form.cleaned_data["impact"],
                    routine_type=form.cleaned_data["routine_type"],
                    is_public=form.cleaned_data["is_public"],
                    set_rest_time=form.cleaned_data["set_rest_time"],
                    exercise_rest_time=form.cleaned_data["exercise_rest_time"],
                )
                routine.save()

                for i, exercise in enumerate(form.cleaned_data["routine"]):
                    db_exercise = Exercise.objects.create(
                        routine=routine,
                        exercise=exercise.get("exercise"),
                        reps=exercise.get("reps"),
                        sets=exercise.get("sets"),
                        duration=exercise.get("duration"),
                        order=i,
                    )
                    db_exercise.save()

                for tag in form.cleaned_data["tags"].split(","):
                    db_tag = RoutineTag.objects.create(
                        routine=routine, tag=tag.strip().replace(" ", "_")
                    )
                    db_tag.save()

                for muscle in form.cleaned_data["target_muscles"]:
                    db_muscle = RoutineTargetMuscle.objects.create(
                        routine=routine, muscle=muscle
                    )
                    db_muscle.save()

                for equipment in form.cleaned_data["equipment"]:
                    db_equipment = RoutineEquipment.objects.create(
                        routine=routine, equipment=equipment
                    )
                    db_equipment.save()
                messages.success(request, "Routine created successfully!")
                return redirect(
                    reverse("update_routine", kwargs={"routine_id": routine.uuid})
                )
            except Exception as error:
                logging.error(error)
                messages.error(request, "An error occurred while creating the routine.")
        else:
            add_error_messages(form, request)
    return render(request, "application/create_routine.html", {"form": form})
