from typing import List, Dict, Optional

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Team, Player, PlayerPosition, PlayerTeam, Coach, CoachTeam


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
    position = serializers.ChoiceField(choices=PlayerPosition.choices)

    class Meta:
        model = PlayerTeam
        fields = ['player', 'team', 'position']

    def validate(self, data):
        if data['team'].team_type == 'NATIONAL':
            if PlayerTeam.objects.filter(
                player=data['player'],
                team__team_type='NATIONAL'
            ).exists():
                raise serializers.ValidationError("A player can only be part of one national team.")
        return data

    def create(self, validated_data):
        return PlayerTeam.objects.create(**validated_data)


class TeamDetailSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()
    coaches = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'home_stadium', 'team_type', 'founded_year', 'country', 'players', 'coaches']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_players(self, obj) -> List[Dict[str, any]]:
        player_teams = PlayerTeam.objects.filter(team=obj).select_related('player')
        return [
            {
                'id': pt.player.id,
                'first_name': pt.player.first_name,
                'last_name': pt.player.last_name,
                'jersey_number': pt.player.jersey_number,
                'position': pt.position
            }
            for pt in player_teams
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_coaches(self, obj) -> List[Dict[str, any]]:
        coach_teams = CoachTeam.objects.filter(team=obj).select_related('coach')
        return [
            {
                'id': ct.coach.id,
                'first_name': ct.coach.first_name,
                'last_name': ct.coach.last_name
            }
            for ct in coach_teams
        ]

class AssignCoachToTeamsSerializer(serializers.Serializer):
    team_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate_team_ids(self, value):
        existing_teams = Team.objects.filter(id__in=value)
        if len(existing_teams) != len(value):
            raise serializers.ValidationError("One or more team IDs are invalid.")
        return value


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'nationality']


class CoachDetailSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'nationality', 'teams']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_teams(self, obj):
        coach_teams = CoachTeam.objects.filter(coach=obj).select_related('team')
        return [
            {
                'id': ct.team.id,
                'name': ct.team.name,
                'team_type': ct.team.team_type
            }
            for ct in coach_teams
        ]


class ChangePlayerPositionSerializer(serializers.ModelSerializer):
    position = serializers.ChoiceField(choices=PlayerPosition.choices)

    class Meta:
        model = PlayerTeam
        fields = ['position']


class FilteredPlayerSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'nationality', 'jersey_number', 'position']

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj) -> Optional[str]:
        team_id = self.context['view'].kwargs['team_id']
        player_team = PlayerTeam.objects.filter(player=obj, team_id=team_id).first()
        return player_team.position if player_team else None