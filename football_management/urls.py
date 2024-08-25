from django.urls import path
from .views import TeamListCreateView, TeamRetrieveUpdateDestroyView

urlpatterns = [
    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyView.as_view(), name='team-detail'),
]