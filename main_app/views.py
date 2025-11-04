from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Event, University,Favorite,Profile
from .serializers import EventSerializer, UniversitySerializer
from django.shortcuts import get_object_or_404
from .serializers import FavoriteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .serializers import UserReadSerializer, UserUpdateSerializer, ProfileSerializer
from django.db import transaction
from django.db.utils import IntegrityError
from .permissions import IsOrganizerOrReadOnly, IsOrganizerForEventOrReadOnly

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserReadSerializer(request.user).data, status=200)

    def put(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError:
            return Response({'detail': 'Username or email already exists'}, status=400)

        return Response(UserReadSerializer(request.user).data, status=200)

    def delete(self, request):
        with transaction.atomic():
            request.user.delete()
        return Response(status=204)



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]   

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class Home(APIView):
    
    def get(self, request):
        content = {'message': 'Welcome to capstone project'}
        return Response(content)
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UniversityList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = University.objects.all().order_by("name")
        return Response(UniversitySerializer(qs, many=True).data, status=200)


class EventIndex(APIView):
    permission_classes = [IsOrganizerOrReadOnly]

    def get(self, request):
        qs = Event.objects.select_related("university").all().order_by("-created_at")
        uni_id = request.GET.get("university")
        q = request.GET.get("q")
        if uni_id:
            qs = qs.filter(university_id=uni_id)
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(location__icontains=q) |
                Q(university__name__icontains=q)
            )
        return Response(EventSerializer(qs, many=True).data, status=200)

    def post(self, request):
        user = request.user
        if not (user.is_authenticated and hasattr(user, "profile") and user.profile.role == "organizer"):
            return Response({'detail': 'Only organizers can create events.'}, status=403)

        data = request.data.copy()
        data["university"] = user.profile.university_id
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(EventSerializer(obj).data, status=201)
        return Response(serializer.errors, status=400)


class EventDetail(APIView):
    permission_classes = [IsOrganizerForEventOrReadOnly]

    def get_obj(self, event_id):
        try:
            return Event.objects.select_related("university").get(id=event_id)
        except Event.DoesNotExist:
            return None

    def get(self, request, event_id):
        ev = self.get_obj(event_id)
        if not ev:
            return Response({'detail': 'Not found.'}, status=404)
        return Response(EventSerializer(ev).data, status=200)

    def put(self, request, event_id):
        ev = self.get_obj(event_id)
        if not ev:
            return Response({'detail': 'Not found.'}, status=404)

        if not (request.user.is_authenticated and hasattr(request.user, "profile") and
                request.user.profile.role == "organizer" and
                request.user.profile.university_id == ev.university_id):
            return Response({'detail': 'Forbidden'}, status=403)

        data = request.data.copy()
        data["university"] = request.user.profile.university_id
        serializer = EventSerializer(ev, data=data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(EventSerializer(obj).data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, event_id):
        ev = self.get_obj(event_id)
        if not ev:
            return Response({'detail': 'Not found.'}, status=404)

        if not (request.user.is_authenticated and hasattr(request.user, "profile") and
                request.user.profile.role == "organizer" and
                request.user.profile.university_id == ev.university_id):
            return Response({'detail': 'Forbidden'}, status=403)

        data = request.data.copy()
        if "university" in data:
            data.pop("university")
        serializer = EventSerializer(ev, data=data, partial=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(EventSerializer(obj).data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, event_id):
        ev = self.get_obj(event_id)
        if not ev:
            return Response({'detail': 'Not found.'}, status=404)

        if not (request.user.is_authenticated and hasattr(request.user, "profile") and
                request.user.profile.role == "organizer" and
                request.user.profile.university_id == ev.university_id):
            return Response({'detail': 'Forbidden'}, status=403)

        ev.delete()
        return Response({"success": True}, status=200)

class FavoriteIndex(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        qs = Favorite.objects.filter(user=user).order_by('-created_at')
        return Response(FavoriteSerializer(qs, many=True).data, status=200)

    def post(self, request):
        user = request.user
        event_id = request.data.get('event')
        if not event_id:
            return Response({'detail': 'event is required'}, status=400)

        event = get_object_or_404(Event, id=event_id)
        fav, created = Favorite.objects.get_or_create(user=user, event=event)
        return Response(FavoriteSerializer(fav).data, status=201 if created else 200)




class FavoriteDetail(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, fav_id):
        fav = get_object_or_404(Favorite, id=fav_id)
        fav.delete()
        return Response(status=204)

class FavoriteByEvent(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, event_id):
        Favorite.objects.filter(event_id=event_id, user=request.user).delete()
        return Response(status=204)







