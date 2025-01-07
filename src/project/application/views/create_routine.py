import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls.base import reverse

from application.forms.routine_form import RoutineForm
from application.utils.form_messages import add_error_messages
from application.models.exercise_routine import ExerciseRoutine


@login_required
def create_routine(request):
    form = RoutineForm()
    if request.method == "POST":
        form = RoutineForm(request.POST)
        if form.is_valid():
            try:
                routine = ExerciseRoutine.create_routine(form, request.user)
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
