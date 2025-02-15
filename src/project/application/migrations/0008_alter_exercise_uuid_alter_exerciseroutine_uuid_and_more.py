# Generated by Django 4.2.17 on 2025-01-04 14:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        (
            "application",
            "0007_rename_estimated_time_exerciseroutine_estimated_duration_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="exercise",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="exerciseroutine",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="routineequipment",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="routinetag",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="routinetargetmuscle",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
