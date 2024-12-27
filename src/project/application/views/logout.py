from django.contrib import messages
from django.contrib.auth import logout as d_logout
from django.shortcuts import redirect


def logout(request):
    d_logout(request)
    messages.success(request, "You have been logged out")
    return redirect("/")
