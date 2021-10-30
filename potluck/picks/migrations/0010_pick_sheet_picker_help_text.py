# Generated by Django 3.1.4 on 2021-07-06 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("picks", "0009_rename_pot_picks_to_pot_picksheets"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picksheet",
            name="picker",
            field=models.CharField(
                help_text="Who is submitting this pick sheet?", max_length=100
            ),
        ),
    ]
