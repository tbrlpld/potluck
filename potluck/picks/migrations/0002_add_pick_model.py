# Generated by Django 3.1.4 on 2021-04-03 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0001_add_pot_model'),
        ('teams', '0001_add_team_model'),
        ('picks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamepick',
            name='picked_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='teams.team'),
        ),
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picker', models.CharField(help_text='Name of the person picking', max_length=100)),
                ('pot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picks', to='pots.pot')),
            ],
        ),
        migrations.AlterField(
            model_name='gamepick',
            name='pick',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_picks', to='picks.pick'),
        ),
    ]
