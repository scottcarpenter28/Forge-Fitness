from django.db import models


class Equipment(models.Model):
    equipment_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.equipment_name

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
