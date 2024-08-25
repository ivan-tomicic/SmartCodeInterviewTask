# In a new file called serializers.py in your app directory

from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'home_stadium', 'team_type', 'founded_year', 'country']
