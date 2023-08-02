from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from contact import views

urlpatterns = [
    # Request to get all users.
    path('', views.ContactList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)