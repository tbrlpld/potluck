# Generated by Django 3.1.4 on 2021-05-24 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("picks", "0006_rename_gamepicktemp_to_pick"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pick",
            old_name="pick",
            new_name="pick_sheet",
        ),
    ]
