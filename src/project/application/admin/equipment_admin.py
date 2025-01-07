from django.contrib import admin


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "equipment_name"]

    class Meta:
        verbose_name = "equipment"
        verbose_name_plural = "equipment"
