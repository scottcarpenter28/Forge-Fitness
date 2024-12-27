from django.db.models import TextChoices
from django.utils.translation import gettext_lazy


class GenderOptions(TextChoices):
    MALE = "Male", gettext_lazy("Male")
    FEMALE = "Female", gettext_lazy("Female")
