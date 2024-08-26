from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Coach, Team, CoachTeam, PlayerTeam
from .serializers import AssignCoachToTeamsSerializer, CoachSerializer, ChangePlayerPositionSerializer

from .models import Team, Player
from .serializers import TeamSerializer, PlayerSerializer, AddPlayerToTeamSerializer, TeamDetailSerializer


class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        serializer.save()


class TeamRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamDetailSerializer
        return TeamSerializer

    def perform_update(self, serializer):
        serializer.save()

class CoachListCreateView(generics.ListCreateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

class CoachRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

class PlayerListCreateView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class AddPlayerToTeamView(generics.CreateAPIView):
    serializer_class = AddPlayerToTeamSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AssignCoachToTeamsView(APIView):
    def post(self, request, coach_id):
        coach = get_object_or_404(Coach, id=coach_id)
        serializer = AssignCoachToTeamsSerializer(data=request.data)

        if serializer.is_valid():
            team_ids = serializer.validated_data['team_ids']
            teams = Team.objects.filter(id__in=team_ids)

            # Create CoachTeam entries
            coach_teams = [CoachTeam(coach=coach, team=team) for team in teams]
            CoachTeam.objects.bulk_create(coach_teams, ignore_conflicts=True)

            return Response({
                "message": f"Coach {coach.first_name} {coach.last_name} assigned to {len(teams)} team(s) successfully."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePlayerPositionView(generics.UpdateAPIView):
    serializer_class = ChangePlayerPositionSerializer

    def get_object(self):
        player_id = self.kwargs['player_id']
        team_id = self.kwargs['team_id']
        return get_object_or_404(PlayerTeam, player_id=player_id, team_id=team_id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "message": f"Position updated successfully for player {instance.player.first_name} {instance.player.last_name} in team {instance.team.name}",
            "new_position": serializer.data['position']
        })