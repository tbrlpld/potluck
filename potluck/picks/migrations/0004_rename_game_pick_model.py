# Generated by Django 3.1.4 on 2021-05-23 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0001_add_team_model"),
        ("games", "0003_add_pot_fk_to_game"),
        ("picks", "0003_auto_20210523_2221"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="GamePick",
            new_name="GamePickTemp",
        ),
    ]
