from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from events import views

urlpatterns = [
    # Request to get all events.
    path('', views.EventsList.as_view(), name='events-list'),
    # Request to get specific event by id.
    path('<int:pk>/', views.EventsDetail.as_view(), name='events-detail'),
    # Request to get all places.
    path('places/', views.PlacesList.as_view(), name='places-list'),
    # Request to get specific place by id.
    path('places/<int:pk>/', views.PlacesDetail.as_view(), name='places-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)