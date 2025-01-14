from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404


@login_required
def run_routine(request, routine_id: str):
    raise Http404("Running routines is not yet implemented.")
