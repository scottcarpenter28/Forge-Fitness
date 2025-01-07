import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls.base import reverse

from application.forms.routine_form import RoutineForm
from application.utils.form_messages import add_error_messages
from application.models.exercise_routine import ExerciseRoutine


@login_required
def update_routine(request, routine_id: str):
    if not routine_id:
        messages.error(request, "Routine ID is required.")
        return redirect("/")

    found_routine = ExerciseRoutine.objects.filter(
        uuid=routine_id, creator=request.user
    ).first()
    if not found_routine:
        messages.error(request, "Routine not found")
        return redirect("/")

    if request.method == "POST":
        form = RoutineForm(request.POST)
        if form.is_valid():
            try:
                found_routine.update_routine(form)
                messages.success(request, "Routine updated.")
            except Exception as error:
                logging.error(error)
                messages.error(request, "An error occurred while updating the routine.")

        else:
            add_error_messages(form, request)

    form = RoutineForm(found_routine.to_dict())
    return render(request, "application/update_routine.html", {"form": form})


@login_required
def delete_routine(request, routine_id: str):
    if not routine_id:
        messages.error(request, "Routine ID is required.")
        return redirect("/")

    found_routine = ExerciseRoutine.objects.filter(
        uuid=routine_id, creator=request.user
    ).first()
    if not found_routine:
        messages.error(request, "Routine not found")
        return redirect("/")

    if request.method == "POST":
        found_routine.delete()
        messages.success(request, "Routine deleted.")
        return redirect("/")

    form = RoutineForm(found_routine.to_dict())
    return redirect(
        reverse("update_routine", kwargs={"routine_id": found_routine.uuid})
    )
