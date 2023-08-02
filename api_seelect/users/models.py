###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.db import models
from django.utils import timezone
from functions.generateRandomHash import generateRandomHash

###########################################################################################
# Models                                                                                  #
###########################################################################################
# Model for user informations.
class User(models.Model): 
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=256, unique=True)
    password = models.CharField(max_length=256, unique=True, null=False, blank=False)
    date_joined = models.DateTimeField(default=timezone.now)

###########################################################################################
# Model for user authentication informations.
class UserAuthentication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='auth')
    password_salt = models.CharField(max_length=16, null=False)
    hash_algorithm = models.CharField(max_length=32, null=False)
    token = models.CharField(max_length=128, null=False, unique=True)
    email_validation = models.BooleanField(default=False)
    token_generation_time = models.DateTimeField(default=timezone.now)

    def refresh_token(self):
        self.token = generateRandomHash()
        self.save()
###########################################################################################