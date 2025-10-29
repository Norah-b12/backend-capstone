from django.db import models


class University(models.Model):
    name = models.CharField(max_length=120, unique=True)
    city = models.CharField(max_length=120, blank=True)
    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="events")
    def __str__(self):
        uni = getattr(self.university, "name", "")
        return f"{self.title} @ {uni}" if uni else self.titl
