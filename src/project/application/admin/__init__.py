from django.contrib import admin

from application.admin.equipment_admin import EquipmentAdmin
from application.admin.muscle_admin import MuscleAdmin
from application.models import Equipment, Muscle

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Muscle, MuscleAdmin)
