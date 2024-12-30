from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def create_routine(request):
    return render(request, "application/create_routine.html")
