from django.shortcuts import render


def login(request, next_route: str = ""):
    if request.method == "POST":
        # Todo: verify user
        pass
    return render(request, "application/login.html")
