import django_filters
from .models import Player, PlayerTeam

class PlayerFilter(django_filters.FilterSet):
    nationality = django_filters.CharFilter(method='filter_nationality')
    position = django_filters.CharFilter(method='filter_position')

    class Meta:
        model = Player
        fields = ['nationality', 'position']

    def filter_nationality(self, queryset, name, value):
        nationalities = [nat.strip() for nat in value.split(',')]
        return queryset.filter(nationality__in=nationalities)

    def filter_position(self, queryset, name, value):
        positions = [pos.strip() for pos in value.split(',')]
        return queryset.filter(playerteam__position__in=positions)