# Generated by Django 2.2.16 on 2021-01-21 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authkeys", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="keyaction",
            name="content_type",
        ),
        migrations.RemoveField(
            model_name="keyaction",
            name="key",
        ),
        migrations.DeleteModel(
            name="Key",
        ),
        migrations.DeleteModel(
            name="KeyAction",
        ),
    ]