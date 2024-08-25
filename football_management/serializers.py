# In a new file called serializers.py in your app directory

from rest_framework import serializers
from .models import Team, Player, PlayerPosition, PlayerTeam


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'home_stadium', 'team_type', 'founded_year', 'country']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'nationality',
                  'jersey_number', 'height', 'market_value']


class AddPlayerToTeamSerializer(serializers.ModelSerializer):
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=PlayerPosition.objects.all())

    class Meta:
        model = PlayerTeam
        fields = ['player', 'team', 'position']

    def validate(self, data):
        # Check if the player is already in a national team if this is a national team
        if data['team'].team_type == 'NATIONAL':
            if PlayerTeam.objects.filter(
                player=data['player'],
                team__team_type='NATIONAL'
            ).exists():
                raise serializers.ValidationError("A player can only be part of one national team.")
        return data