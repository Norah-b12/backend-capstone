from django.urls import path
from .views import Home, EventIndex, EventDetail, UniversityList,FavoriteIndex,FavoriteDetail,FavoriteByEvent, CreateUserView, WhoAmI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('events/', EventIndex.as_view(), name='event-index'),
    path('events/<int:event_id>/', EventDetail.as_view(), name='event-detail'),
    path('universities/', UniversityList.as_view(), name='university-index'),
    path('favorites/', FavoriteIndex.as_view(), name='favorite-index'),
    path('favorites/<int:fav_id>/', FavoriteDetail.as_view(), name='favorite-detail'),
    path('favorites/by-event/<int:event_id>/', FavoriteByEvent.as_view(), name='favorite-by-event'),

    path('auth/signup/', CreateUserView.as_view(), name='signup'), 
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', WhoAmI.as_view(), name='whoami'),

  ]
