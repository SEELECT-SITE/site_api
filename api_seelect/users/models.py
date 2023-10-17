###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.db import models
from django.utils import timezone
from utils.functions.generateRandomHash import generateRandomHash
from django.core.validators import MaxValueValidator

###########################################################################################
# Models                                                                                  #
###########################################################################################
# Model for user informations.
class User(models.Model): 
    role = models.CharField(max_length=64, blank=False, null=False, default='user')
    email = models.EmailField(max_length=256, unique=True)
    password = models.CharField(max_length=256, unique=True, null=False, blank=False)
    date_joined = models.DateTimeField(default=timezone.now)

###########################################################################################
# Model for user informations.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='profile')
    first_name = models.CharField(max_length=64, blank=True, default='')
    last_name = models.CharField(max_length=64, blank=True, default='')
    ies = models.CharField(max_length=256, blank=True, default='')
    birthday = models.DateField(blank=True, null=False, default="2000-01-01")
    cpf = models.CharField(max_length=11, blank=True, null=False, default='')
    course = models.CharField(max_length=256, blank=True, default='')
    semester = models.PositiveIntegerField(validators=[MaxValueValidator(48)], blank=True, default=0)

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
        self.token_generation_time = timezone.now()
        self.save()
###########################################################################################