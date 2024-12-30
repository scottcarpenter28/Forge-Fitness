from django.db.models import TextChoices
from django.utils.translation import gettext_lazy


class RoutineOptions(TextChoices):
    CARDIO = "Cardio", gettext_lazy("Cardio")
    Strength = "Strength", gettext_lazy("Strength")
