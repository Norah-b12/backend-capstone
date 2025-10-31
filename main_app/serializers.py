from rest_framework import serializers
from .models import Event, University,Favorite

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source="university.name", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "time",
            "location",
            "university",
            "university_name",
            "created_at"
        ]

class FavoriteSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    university_name = serializers.CharField(source='event.university.name', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'event', 'event_title', 'university_name', 'created_at']
        read_only_fields = ['id', 'created_at']
