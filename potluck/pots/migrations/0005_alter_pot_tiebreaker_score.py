# Generated by Django 3.2.6 on 2021-11-12 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0004_pot_tiebreaker_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pot',
            name='tiebreaker_score',
            field=models.PositiveSmallIntegerField(help_text='Enter the tiebreaker score.', null=True),
        ),
    ]
