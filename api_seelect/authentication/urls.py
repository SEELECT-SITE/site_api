from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from authentication import views

urlpatterns = [
    # Request to get all users.
    path('register/', views.Register.as_view()),
    # Request to validate the login and password.
    path('login/', views.login),
    # Request to get user information using the token.
    #path('loadSession/', views.loadSession)
]

urlpatterns = format_suffix_patterns(urlpatterns)