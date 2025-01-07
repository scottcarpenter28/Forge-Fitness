from django.contrib import admin


class MuscleAdmin(admin.ModelAdmin):
    list_display = ["id", "muscle_name"]
