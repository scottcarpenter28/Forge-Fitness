from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http.request import HttpRequest


def login_user(request: HttpRequest, username: str, password: str) -> bool:
    """
    Logs a user in.
    :param request: The current request.
    :param username: The name of the user to login.
    :param password: The password for the user.
    :return: True if the login was successful, False otherwise.
    """
    authenticated_user = authenticate(username=username, password=password)
    if authenticated_user is None:
        messages.error(request, "Username or password is incorrect.")
        return False
    elif authenticated_user.is_active:
        login(request, authenticated_user)
        return True
    else:
        messages.error(request, "Your account has been disabled.")
    return False
