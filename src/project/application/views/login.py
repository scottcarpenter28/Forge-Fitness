from django.contrib import messages
from django.shortcuts import render, redirect

from application.utils.login_user import login_user


def login(request, next_route: str = "/"):
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        password = post_data.get("password")
        if username is None:
            messages.error(request, "Username is required.")
        elif password is None:
            messages.error(request, "Password is required.")
        else:
            if login_user(request, username, password):
                return redirect(next_route)
    return render(request, "application/login.html")
