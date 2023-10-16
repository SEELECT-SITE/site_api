###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

from users.models import UserProfile
from events.models import Events

###########################################################################################
# Models                                                                                  #
###########################################################################################
# Model for kits informations.
class Kits(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=False)
    is_payed = models.BooleanField(blank=False, default=False)
    model = models.CharField(max_length=24, blank=False, null=False)
    events = models.ManyToManyField(Events, through='KitsEvents')
    date_created = models.DateTimeField(default=timezone.now)

###########################################################################################
# Model to relate kits and events
class KitsEvents(models.Model):
    kit = models.ForeignKey(Kits, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

###########################################################################################