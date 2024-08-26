from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Coach, Team, CoachTeam
from .serializers import AssignCoachToTeamsSerializer

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

class PlayerCreateView(generics.CreateAPIView):
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