from django.test import TestCase
from django.contrib.auth.models import User

from application.forms.account_creation import AccountCreationForm


class TestAccountForm(TestCase):
    def setUp(self):
        self.form_data = {
            "email": "test@email.com",
            "username": "test",
            "password": "password",
            "confirm_password": "password",
            "preferred_units": "Metric",
            "gender": "Male",
        }

    def test_normal_account_creation(self):
        form = AccountCreationForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_password_clean_fail(self):
        self.form_data["password"] = "<PASSWORD>"
        form = AccountCreationForm(self.form_data)
        self.assertFalse(form.is_valid())

    def test_username_already_used(self):
        User.objects.create_user("test", "<EMAIL>", "password")
        form = AccountCreationForm(self.form_data)
        self.assertFalse(form.is_valid())

    def test_email_already_used(self):
        User.objects.create_user("another_name", "test@email.com", "password")
        form = AccountCreationForm(self.form_data)
        self.assertFalse(form.is_valid())
