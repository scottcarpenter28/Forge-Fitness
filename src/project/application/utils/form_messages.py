from django.contrib import messages
from django.forms import Form
from django.http.request import HttpRequest


def add_error_messages(form: Form, request: HttpRequest) -> None:
    """
    Loops through all failed validations for the form and creates a message to be displayed to the user.
    :param form: The form to pull error messages from.
    :param request: The current HTTP request.
    :return: None.
    """
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, error)
