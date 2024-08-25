from django.db import models
from django.core.exceptions import ValidationError

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Team(models.Model):
    TEAM_TYPES = (
        ('CLUB', 'Club'),
        ('NATIONAL', 'National'),
    )

    name = models.CharField(max_length=100, unique=True)
    home_stadium = models.CharField(max_length=100)
    team_type = models.CharField(max_length=10, choices=TEAM_TYPES)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PlayerPosition(models.TextChoices):
    GK = 'GK', 'Goalkeeper'
    CB = 'CB', 'Center Back'
    LB = 'LB', 'Left Full-Back'
    RB = 'RB', 'Right Full-Back'
    RWB = 'RWB', 'Right Wing-Back'
    LWB = 'LWB', 'Left Wing-Back'
    CDM = 'CDM', 'Defensive Midfielder'
    CM = 'CM', 'Centre Midfielder'
    CAM = 'CAM', 'Central Attacking Midfielder'
    LM = 'LM', 'Left Side Midfielder'
    RM = 'RM', 'Right Side Midfielder'
    LW = 'LW', 'Left Winger'
    RW = 'RW', 'Right Winger'
    CF = 'CF', 'Centre Forward'
    RF = 'RF', 'Right Side Forward'
    LF = 'LF', 'Left Side Forward'
    ST = 'ST', 'Striker'

class Player(Person):
    jersey_number = models.PositiveIntegerField()
    teams = models.ManyToManyField(Team, through='PlayerTeam', related_name='players')
    height = models.PositiveIntegerField(help_text="Height in cm", null=True, blank=True)
    market_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

class Coach(Person):
    teams = models.ManyToManyField(Team, through='CoachTeam', related_name='coaches')

class PlayerTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=3, choices=PlayerPosition.choices)

    class Meta:
        unique_together = ('player', 'team')

    def clean(self):
        if self.team.team_type == 'NATIONAL' and PlayerTeam.objects.filter(
            player=self.player,
            team__team_type='NATIONAL'
        ).exclude(pk=self.pk).exists():
            raise ValidationError("A player can only be part of one national team.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class CoachTeam(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('coach', 'team')