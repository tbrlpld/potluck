# Generated by Django 3.2.9 on 2021-12-06 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0006_home_and_away_team"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="teams",
        ),
    ]
