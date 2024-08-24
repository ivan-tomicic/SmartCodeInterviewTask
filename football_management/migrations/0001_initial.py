# Generated by Django 5.1 on 2024-08-25 00:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('nationality', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('nationality', models.CharField(max_length=100)),
                ('jersey_number', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('home_stadium', models.CharField(max_length=100)),
                ('team_type', models.CharField(choices=[('CLUB', 'Club'), ('NATIONAL', 'National')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_management.player')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='football_management.playerposition')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_management.team')),
            ],
            options={
                'unique_together': {('player', 'team')},
            },
        ),
        migrations.AddField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(related_name='players', through='football_management.PlayerTeam', to='football_management.team'),
        ),
        migrations.CreateModel(
            name='CoachTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_management.coach')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_management.team')),
            ],
            options={
                'unique_together': {('coach', 'team')},
            },
        ),
        migrations.AddField(
            model_name='coach',
            name='teams',
            field=models.ManyToManyField(related_name='coaches', through='football_management.CoachTeam', to='football_management.team'),
        ),
    ]
