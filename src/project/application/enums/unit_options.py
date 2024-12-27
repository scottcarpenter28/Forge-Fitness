from django.db.models import TextChoices
from django.utils.translation import gettext_lazy


class UnitOptions(TextChoices):
    METRIC = "Metric", gettext_lazy("Metric")
    IMPERIAL = "Imperial", gettext_lazy("Imperial")
