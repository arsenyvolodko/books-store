# Generated by Django 4.2.11 on 2024-03-15 14:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("feedback_form", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="feedback",
            old_name="mail",
            new_name="email",
        ),
    ]
