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

    def __str__(self):
        return self.name

class PlayerPosition(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Player(Person):
    jersey_number = models.PositiveIntegerField()
    teams = models.ManyToManyField(Team, through='PlayerTeam', related_name='players')

class Coach(Person):
    teams = models.ManyToManyField(Team, through='CoachTeam', related_name='coaches')

class PlayerTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.ForeignKey(PlayerPosition, on_delete=models.PROTECT)

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