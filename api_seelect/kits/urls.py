from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from kits import views

urlpatterns = [
    # Request to get all kits.
    path('', views.KitsList.as_view(), name='kits-list'),
    # Request to get specific kit by id.
    path('<int:pk>/', views.KitsDetail.as_view(), name='kits-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)