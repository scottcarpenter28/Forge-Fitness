from django.contrib import messages
from django.contrib.auth import authenticate, login as d_login
from django.shortcuts import render, redirect


def login(request, next_route: str = "/"):
    authenticated_user = None
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        if username is None:
            messages.error(request, "Username is required.")
        password = post_data.get("password")
        if password is None:
            messages.error(request, "Password is required.")
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is None:
            messages.error(request, "Username or password is incorrect.")

    if authenticated_user is not None and authenticated_user.is_active:
        d_login(request, authenticated_user)
        return redirect(next_route)
    return render(request, "application/login.html")
