# Generated by Django 3.1.4 on 2021-07-06 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0002_pot_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pot',
            name='name',
            field=models.CharField(help_text='What shall we call the pot?', max_length=250),
        ),
    ]
