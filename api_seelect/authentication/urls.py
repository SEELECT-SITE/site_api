from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from authentication import views

urlpatterns = [
    # Request to register a new user.
    path('register/', views.register, name='register'),
    # Request to validate the login and password.
    path('login/', views.login, name='login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)