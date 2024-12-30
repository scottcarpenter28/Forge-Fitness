from django.db import models


class Muscle(models.Model):
    muscle_name = models.CharField(max_length=255)

    def __str__(self):
        return self.muscle_name
