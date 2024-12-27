from django import forms
from django.contrib.auth.models import User

from application.enums.unit_options import UnitOptions
from application.enums.genders import GenderOptions


class AccountCreationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )
    preferred_units = forms.ChoiceField(choices=UnitOptions.choices)
    gender = forms.ChoiceField(choices=GenderOptions.choices)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise forms.ValidationError("Username already in use")
        return self.cleaned_data["username"]

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("Email already in use")
        return self.cleaned_data["email"]

    def clean_confirm_password(self):
        if not self.cleaned_data["password"] == self.cleaned_data["confirm_password"]:
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data["confirm_password"]
