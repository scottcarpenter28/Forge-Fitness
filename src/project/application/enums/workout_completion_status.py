from django.db.models import TextChoices
from django.utils.translation import gettext_lazy


class WorkoutCompletionStatus(TextChoices):
    COMPLETED = "Completed", gettext_lazy("Completed")
    INCOMPLETE = "Incomplete", gettext_lazy("Incomplete")
    NOT_STARTED = "Not Started", gettext_lazy("Not Started")
