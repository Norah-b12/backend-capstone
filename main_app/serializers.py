from rest_framework import serializers
from .models import Event, University,Favorite, Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
    )
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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'role', 'university']
        read_only_fields = ['role', 'university']


class UserReadSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    favorites = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'favorites']

    def get_favorites(self, user):
        qs = Favorite.objects.filter(user=user).select_related('event', 'event__university')
        return FavoriteSerializer(qs, many=True).data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']