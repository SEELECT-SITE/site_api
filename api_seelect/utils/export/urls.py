# Imports
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    # Request to export all users in csv.
    path('export_users/', export_users, name='export-users'),
    # Request to get all events in csv.
    path('export_events/', export_events, name='export-events'),
    # Request to get all kits in csv.
    path('export_kits/', export_kits, name='export-kits'),
]

urlpatterns = format_suffix_patterns(urlpatterns)