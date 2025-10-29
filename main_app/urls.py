from django.urls import path
from .views import Home, EventIndex, EventDetail, UniversityList
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('events/', EventIndex.as_view(), name='event-index'),
    path('events/<int:event_id>/', EventDetail.as_view(), name='event-detail'),
    path('universities/', UniversityList.as_view(), name='university-index'),
]
