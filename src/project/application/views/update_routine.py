import logging
from typing import Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse

from application.forms.routine_form import RoutineForm
from application.utils.form_messages import add_error_messages
from application.models.exercise_routine import ExerciseRoutine


@login_required
def update_routine(
    request: WSGIRequest, routine_id: str
) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Updates the matching routine for the user.
    :param request: Information about the request.
    :param routine_id: The routine to update.
    :return: The updated form, or redirect to root if not found.
    """
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
    return render(
        request,
        "application/update_routine.html",
        {"form": form, "routine": found_routine},
    )


@login_required
def delete_routine(request: WSGIRequest, routine_id: str) -> HttpResponseRedirect:
    """
    Deletes a routine.
    :param request: Information about the request.
    :param routine_id: The routine to delete.
    :return: Redirects to root once action is completed.
    """
    if not routine_id:
        messages.error(request, "Routine ID is required.")
        return redirect("/")

    if request.method == "POST":
        found_routine = ExerciseRoutine.objects.filter(
            uuid=routine_id, creator=request.user
        ).first()

        if not found_routine:
            messages.error(request, "Routine not found")
        else:
            found_routine.delete()
            messages.success(request, "Routine deleted.")
        return redirect(reverse("my_routines"))

    messages.warning(request, "Method not allowed.")
    return redirect("/")
