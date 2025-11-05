from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Event, University, Favorite

class ModelsTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name="Test Uni", city="Test City")
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.profile = self.user.profile
        self.profile.role = "organizer"
        self.profile.university = self.uni
        self.profile.save()
        self.event1 = Event.objects.create(
            title="Event 1",
            description="Desc 1",
            date="2025-12-01",
            time="12:00",
            location="Hall 1",
            university=self.uni
        )
        self.event2 = Event.objects.create(
            title="Event 2",
            description="Desc 2",
            date="2025-12-02",
            time="13:00",
            location="Hall 2",
            university=self.uni
        )
        self.favorite = Favorite.objects.create(user=self.user, event=self.event1)

    def test_event_creation(self):
        self.assertEqual(self.event1.title, "Event 1")
        self.assertEqual(self.event1.university, self.uni)

    def test_favorite_creation(self):
        self.assertEqual(self.favorite.user, self.user)
        self.assertEqual(self.favorite.event, self.event1)

    def test_user_profile_auto_created(self):
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.profile.role, "organizer")
        self.assertEqual(self.user.profile.university, self.uni)
