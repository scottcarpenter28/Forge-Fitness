import uuid

from django.contrib.auth.models import User
from django.db import models


class UserPreferences(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    units = models.CharField(max_length=10)
