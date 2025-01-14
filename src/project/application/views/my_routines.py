from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from application.models.exercise_routine import ExerciseRoutine


@login_required
def my_routines(request):
    user_routines = ExerciseRoutine.objects.filter(creator=request.user).all()
    return render(request, "application/my_routines.html", {"routines": user_routines})
