from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from authentication import views

urlpatterns = [
    # Request to register a new user.
    path('register/', views.register, name='register'),
    # Request to validate the login and password.
    path('login/', views.login, name='login'),
    # Request to validate email
    path('email_validation/', views.email_validation, name='email-validation'),
    # Request to change password when you forget
    path('forget_password/', views.forget_password, name='forget-password'),
    # Request to change password
    path('change_password/', views.change_password, name='change-password'),
    # Request to change role
    path('change_role/', views.change_role, name='change-role'),
]

urlpatterns = format_suffix_patterns(urlpatterns)