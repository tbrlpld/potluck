# Generated by Django 3.2.6 on 2021-10-31 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("picks", "0010_pick_sheet_picker_help_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="picksheet",
            name="tiebreaker_guess",
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
