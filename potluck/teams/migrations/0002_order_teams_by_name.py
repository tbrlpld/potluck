# Generated by Django 3.1.4 on 2021-07-07 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0001_add_team_model"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ["name"]},
        ),
    ]
