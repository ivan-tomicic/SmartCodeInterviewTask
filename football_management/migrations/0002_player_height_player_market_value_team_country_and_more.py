# Generated by Django 5.1 on 2024-08-25 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='height',
            field=models.PositiveIntegerField(blank=True, help_text='Height in cm', null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='market_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='country',
            field=models.CharField(default='None', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='founded_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
