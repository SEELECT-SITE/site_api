###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

###########################################################################################
# Models                                                                                  #
###########################################################################################
# Model for places informations.
class Places(models.Model):
    location = models.CharField(max_length=64, blank=True)
    url_location = models.CharField(max_length=1024, )
    capacity = models.PositiveIntegerField(validators=[MaxValueValidator(100000)], blank=False, null=False)
    equipaments = models.CharField(max_length=4096, blank=True, null=False)
    date_created = models.DateTimeField(default=timezone.now)

###########################################################################################
# Model for event informations.
class Events(models.Model): 
    title = models.CharField(max_length=256, blank=True)
    category = models.CharField(max_length=256, blank=True)
    number_of_inscriptions = models.PositiveIntegerField(validators=[MaxValueValidator(1000)], blank=False, null=False, default=0)
    max_number_of_inscriptions = models.PositiveIntegerField(validators=[MaxValueValidator(1000)], blank=False, null=False)
    place = models.ManyToManyField(Places, through='EventsPlaces')
    course_time = models.CharField(max_length=24, blank=True, null=True, default='00:00:00-00:00:00')
    date_start = models.DateTimeField(default='2023-12-12T00:00:00.000000Z')
    date_end = models.DateTimeField(default='2023-12-12T00:00:00.000000Z')
    date_created = models.DateTimeField(default=timezone.now)

    def newInscription(self):
        if (self.number_of_inscriptions < self.max_number_of_inscriptions):
            self.number_of_inscriptions += 1
            self.save()
            return True
        else:
            return None
    
    def deleteInscription(self):
        self.number_of_inscriptions -= 1
        self.save()

###########################################################################################
# Model to relate events and places
class EventsPlaces(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
###########################################################################################