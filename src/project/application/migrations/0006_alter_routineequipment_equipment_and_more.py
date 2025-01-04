# Generated by Django 4.2.17 on 2025-01-04 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0005_routineequipment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="routineequipment",
            name="equipment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="application.equipment"
            ),
        ),
        migrations.AlterField(
            model_name="routinetargetmuscle",
            name="muscle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="application.muscle"
            ),
        ),
    ]
