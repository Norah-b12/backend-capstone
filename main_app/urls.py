from django.urls import path
from .views import Home, EventIndex, EventDetail, UniversityList,FavoriteIndex,FavoriteDetail,FavoriteByEvent
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('events/', EventIndex.as_view(), name='event-index'),
    path('events/<int:event_id>/', EventDetail.as_view(), name='event-detail'),
    path('universities/', UniversityList.as_view(), name='university-index'),
    path('favorites/', FavoriteIndex.as_view(), name='favorite-index'),
    path('favorites/<int:fav_id>/', FavoriteDetail.as_view(), name='favorite-detail'),
    path('favorites/by-event/<int:event_id>/', FavoriteByEvent.as_view(), name='favorite-by-event'),


]
