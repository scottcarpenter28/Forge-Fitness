from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from application.models.exercise_routine import ExerciseRoutine


@login_required
def run_routine(request, routine_id: str):
    if not routine_id:
        messages.error(request, "Routine ID is required.")
        return redirect("/")

    found_routine = ExerciseRoutine.objects.filter(
        uuid=routine_id, creator=request.user
    ).first()
    if not found_routine:
        messages.error(request, "Routine not found.")
        return redirect("/")

    if not found_routine.is_public:
        if not found_routine.creator == request.user:
            messages.error(request, "You do not have access to this routine.")
            return redirect("/")
    return render(request, "application/run_routine.html", {"routine": found_routine})
