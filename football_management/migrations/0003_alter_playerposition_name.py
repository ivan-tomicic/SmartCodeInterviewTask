# Generated by Django 5.1 on 2024-08-25 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_management', '0002_player_height_player_market_value_team_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerposition',
            name='name',
            field=models.CharField(choices=[('GK', 'Goalkeeper'), ('CB', 'Center Back'), ('LB', 'Left Full-Back'), ('RB', 'Right Full-Back'), ('RWB', 'Right Wing-Back'), ('LWB', 'Left Wing-Back'), ('CDM', 'Defensive Midfielder'), ('CM', 'Centre Midfielder'), ('CAM', 'Central Attacking Midfielder'), ('LM', 'Left Side Midfielder'), ('RM', 'Right Side Midfielder'), ('LW', 'Left Winger'), ('RW', 'Right Winger'), ('CF', 'Centre Forward'), ('RF', 'Right Side Forward'), ('LF', 'Left Side Forward'), ('ST', 'Striker')], max_length=3, unique=True),
        ),
    ]
