# Generated by Django 4.2.11 on 2024-03-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feedback_form", "0003_alter_feedback_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="phone",
            field=models.CharField(max_length=13),
        ),
    ]
