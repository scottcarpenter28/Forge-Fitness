from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from application.forms.routine_form import RoutineForm


@login_required
def create_routine(request, routine_id: Optional[str] = None):
    # Todo: If a routine_id is provided, find the routine

    form = RoutineForm()
    if request.method == "POST":
        form = RoutineForm(request.POST)
        if form.is_valid():
            pass
    messages.error(request, "This is a test")
    return render(request, "application/create_routine.html", {"form": form})
