# Generated by Django 3.2.6 on 2021-11-13 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pots", "0009_update_tiebreaker_description_help_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pot",
            name="tiebreaker_description",
            field=models.CharField(
                default="Total score of the Monday night game",
                help_text='Describe the tiebreaker score you want to use for the pot. For example: "Total score of the Monday night game". In case of a tie, the submission with the closest guess to the score wins.',  # noqa: E501
                max_length=500,
            ),
        ),
    ]
