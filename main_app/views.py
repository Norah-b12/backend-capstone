from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from .models import Event, University
from .serializers import EventSerializer, UniversitySerializer

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to capstone project'}
        return Response(content)
class UniversityList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = University.objects.all().order_by("name")
        return Response(UniversitySerializer(qs, many=True).data, status=200)


class EventIndex(APIView):
    permission_classes = [permissions.AllowAny]

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
        s = EventSerializer(data=request.data)
        if s.is_valid():
            obj = s.save()
            return Response(EventSerializer(obj).data, status=201)
        return Response(s.errors, status=400)


class EventDetail(APIView):
    permission_classes = [permissions.AllowAny]

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
        s = EventSerializer(ev, data=request.data, partial=False)
        if s.is_valid():
            obj = s.save()
            return Response(EventSerializer(obj).data, status=200)
        return Response(s.errors, status=400)

    def patch(self, request, event_id):
        ev = self.get_obj(event_id)
        if not ev:
            return Response({'detail': 'Not found.'}, status=404)
        s = EventSerializer(ev, data=request.data, partial=True)
        if s.is_valid():
            obj = s.save()
            return Response(EventSerializer(obj).data, status=200)
        return Response(s.errors, status=400)

    def delete(self, request, event_id):
        ev = self.get_obj(event_id)
        if not ev:
            return Response({'detail': 'Not found.'}, status=404)
        ev.delete()
        return Response({"success": True}, status=200)






