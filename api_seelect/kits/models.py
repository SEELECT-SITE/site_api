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
# Model for kits types.
class KitModels(models.Model):
    model = models.CharField(max_length=24, blank=False, null=False)
    price = models.IntegerField(blank=True, default=0)
    all_speeches = models.BooleanField(blank=False, null=False, default=False)
    workshops = models.IntegerField(blank=True, default=0)
    bucks_coup = models.BooleanField(blank=False, null=False, default=False)
    description = models.TextField(blank=True, default='')

###########################################################################################
# Model for kits informations.
class Kits(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=False)
    discount = models.IntegerField(blank=True, default=0)
    is_payed = models.BooleanField(blank=False, default=False)
    model = models.ForeignKey(KitModels, on_delete=models.CASCADE, null=False, blank=False, default=1)
    events = models.ManyToManyField(Events, through='KitsEvents')
    date_created = models.DateTimeField(default=timezone.now)

###########################################################################################
# Model to relate kits and events
class KitsEvents(models.Model):
    kit = models.ForeignKey(Kits, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

###########################################################################################
# Discount
class KitsDiscount(models.Model):
    discount = models.IntegerField(blank=True, default=0)
    email = models.EmailField(max_length=512, unique=True)

###########################################################################################