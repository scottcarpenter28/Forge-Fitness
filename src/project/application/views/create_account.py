import logging

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from application.forms.account_creation import AccountCreationForm
from application.models.user_preferences import UserPreferences
from application.utils.form_messages import add_error_messages
from application.utils.login_user import login_user


def create_account(request):
    form = AccountCreationForm()
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                user_preferences = UserPreferences(
                    user=user,
                    gender=form.cleaned_data["gender"],
                    units=form.cleaned_data["preferred_units"],
                )
                user.save()
                user_preferences.save()
                messages.success(request, "Account created successfully!")

                if login_user(
                    request,
                    form.cleaned_data["username"],
                    form.cleaned_data["password"],
                ):
                    return redirect("/")
                else:
                    messages.error(request, "An error occurred while logging in!")
                    return redirect("/")
            except Exception as e:
                logging.error(e)
                messages.error(
                    request, "An error occurred while creating your account."
                )
        else:
            add_error_messages(form, request)
    return render(request, "application/create_account.html", {"form": form})
