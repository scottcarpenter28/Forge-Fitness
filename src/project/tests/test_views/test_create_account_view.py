from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls.base import reverse

from application.models.user_preferences import UserPreferences


class TestAccountCreationView(TestCase):
    def setUp(self):
        self.form_data = {
            "email": "test@email.com",
            "username": "test",
            "password": "password",
            "confirm_password": "password",
            "preferred_units": "Metric",
            "gender": "Male",
        }
        self.client = Client()

    def test_form_error(self):
        User.objects.create_user("test", "<EMAIL>", "password")
        response = self.client.post(reverse("create_account"), self.form_data)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == "Username already in use"

    def test_form_success(self):
        response = self.client.post(reverse("create_account"), self.form_data)
        messages = list(get_messages(response.wsgi_request))

        assert len(messages) == 1
        assert str(messages[0]) == "Account created successfully!"

        created_user_preference = UserPreferences.objects.all().first()
        assert created_user_preference.units == self.form_data["preferred_units"]
        assert created_user_preference.gender == self.form_data["gender"]
