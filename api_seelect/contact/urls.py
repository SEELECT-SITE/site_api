# Imports
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from contact import views

urlpatterns = [
    # Request to get all contact messages.
    path('', views.ContactList.as_view(), name='contact-list'),
    # Request to get specific contact message by id.
    path('<int:pk>/', views.ContactDetail.as_view(), name='contact-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)