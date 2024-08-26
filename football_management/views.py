from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .filters import PlayerFilter
from django_filters import rest_framework as django_filters
from .models import Coach, Team, CoachTeam, PlayerTeam
from .serializers import AssignCoachToTeamsSerializer, CoachSerializer, ChangePlayerPositionSerializer, \
    FilteredPlayerSerializer, CoachDetailSerializer

from .models import Team, Player
from .serializers import TeamSerializer, PlayerSerializer, AddPlayerToTeamSerializer, TeamDetailSerializer


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ['name', 'home_stadium', 'country']

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [CustomSearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'founded_year', 'country']
    search_fields = ['name', 'home_stadium', 'country']

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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CoachDetailSerializer
        return CoachSerializer

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
    @extend_schema(
        request=AssignCoachToTeamsSerializer,
        responses={201: dict},
        description="Assign a coach to multiple teams."
    )
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
    http_method_names = ['put']

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

class FilterPlayersInTeamView(generics.ListAPIView):
    serializer_class = FilteredPlayerSerializer
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = PlayerFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(name='team_id', description='ID of the team', required=True, type=int,
                             location=OpenApiParameter.PATH),
            OpenApiParameter(name='nationality', description='Comma-separated list of nationalities', required=False,
                             type=str),
            OpenApiParameter(name='position', description='Comma-separated list of positions', required=False,
                             type=str),
        ],
        description='Retrieve a list of players in a team, with optional filtering by nationality and position.',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # just to remove the warning from drf-spectacular
            return Player.objects.none()
        team_id = self.kwargs.get('team_id')
        if team_id is not None:
            return Player.objects.filter(teams__id=team_id).distinct()
        return Player.objects.none()


class RemoveCoachFromTeamView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='coach_id', description='ID of the coach', required=True, type=int,
                             location=OpenApiParameter.PATH),
            OpenApiParameter(name='team_id', description='ID of the team', required=True, type=int,
                             location=OpenApiParameter.PATH),
        ],
        description="Remove a coach from a specific team.",
        responses={204: None}
    )
    def delete(self, request, coach_id, team_id):
        coach_team = get_object_or_404(CoachTeam, coach_id=coach_id, team_id=team_id)
        coach_team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RemovePlayerFromTeamView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='player_id', description='ID of the player', required=True, type=int,
                             location=OpenApiParameter.PATH),
            OpenApiParameter(name='team_id', description='ID of the team', required=True, type=int,
                             location=OpenApiParameter.PATH),
        ],
        description="Remove a player from a specific team.",
        responses={204: None}
    )
    def delete(self, request, player_id, team_id):
        player_team = get_object_or_404(PlayerTeam, player_id=player_id, team_id=team_id)
        player_team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)