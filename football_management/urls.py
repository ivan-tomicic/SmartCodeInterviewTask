from django.urls import path
from .views import TeamListCreateView, TeamRetrieveUpdateDestroyView, AddPlayerToTeamView, \
    AssignCoachToTeamsView, CoachListCreateView, CoachRetrieveUpdateDestroyView, PlayerRetrieveUpdateDestroyView, \
    PlayerListCreateView

urlpatterns = [
    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyView.as_view(), name='team-detail'),
    path('players/add-to-team/', AddPlayerToTeamView.as_view(), name='add-player-to-team'),
    path('coaches/<int:coach_id>/assign-teams/', AssignCoachToTeamsView.as_view(), name='assign-coach-to-teams'),
    path('coaches/', CoachListCreateView.as_view(), name='coach-list-create'),
    path('coaches/<int:pk>/', CoachRetrieveUpdateDestroyView.as_view(), name='coach-detail'),
    path('players/', PlayerListCreateView.as_view(), name='player-list-create'),
    path('players/<int:pk>/', PlayerRetrieveUpdateDestroyView.as_view(), name='player-detail'),
]