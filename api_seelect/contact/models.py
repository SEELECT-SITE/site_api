###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.db import models
from django.utils import timezone

###########################################################################################
# Models                                                                                  #
###########################################################################################
# Model for user informations.
class Contact(models.Model): 
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=256)
    phone = models.CharField(max_length=16)
    message = models.CharField(max_length=1024)
    date = models.DateTimeField(default=timezone.now)