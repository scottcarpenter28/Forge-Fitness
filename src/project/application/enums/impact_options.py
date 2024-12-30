from django.db.models import TextChoices
from django.utils.translation import gettext_lazy


class ImpactOptions(TextChoices):
    LOW = "Low", gettext_lazy("Low")
    MEDIUM = "Medium", gettext_lazy("Medium")
    HIGH = "High", gettext_lazy("High")
