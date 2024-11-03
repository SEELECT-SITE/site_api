###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

from users.models import UserProfile

###########################################################################################
# Models                                                                                  #
###########################################################################################
# Model for places informations.
class Places(models.Model):
    location = models.CharField(max_length=64, blank=True)
    url_location = models.CharField(max_length=1024, blank=True, null=True, default='')
    capacity = models.PositiveIntegerField(validators=[MaxValueValidator(100000)], blank=False, null=False, default=0)
    equipaments = models.TextField(blank=True, null=False)
    date_created = models.DateTimeField(default=timezone.now)

###########################################################################################
# Model for event informations.
class Events(models.Model): 
    title = models.CharField(max_length=256, blank=True)
    host = models.CharField(max_length=256, blank=True, null=False, default='')
    category = models.CharField(max_length=256, blank=True, default='')
    number_of_inscriptions = models.PositiveIntegerField(validators=[MaxValueValidator(1000)], blank=False, null=False, default=0)
    max_number_of_inscriptions = models.PositiveIntegerField(validators=[MaxValueValidator(1000)], blank=False, null=False, default=20)
    place = models.ManyToManyField(Places, through='EventsPlaces')
    date = models.JSONField(blank=True, default=dict)
    description = models.TextField(blank=True, null=False, default="")
    date_created = models.DateTimeField(default=timezone.now)

    # Function to increment the inscription number of the event.
    def newInscription(self):
        if (self.number_of_inscriptions < self.max_number_of_inscriptions):
            self.number_of_inscriptions += 1
            self.save()
            return True
        else:
            return None
    
    # Function to decrement the inscription number of the event.
    def deleteInscription(self):
        self.number_of_inscriptions -= 1
        self.save()
        
###########################################################################################
# Model to relate events and places
class EventsPlaces(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    
###########################################################################################
# Model for attendance lists associated with events.
class AttendanceList(models.Model):
    event = models.OneToOneField(Events, on_delete=models.CASCADE, related_name='attendance_list')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Attendance List for {self.event.title}"

###########################################################################################
# Model for attendance associated with attendance list.
class Attendance(models.Model):
    attendance_list = models.ForeignKey(AttendanceList, on_delete=models.CASCADE, related_name='attendances')
    participant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    days = models.JSONField(blank=True, default=list)  # List of booleans indicating presence per day
    hours_per_day = models.JSONField(blank=True, default=list)  # Optional list of hours per day

    def __str__(self):
        return f"Attendance for {self.participant.first_name} {self.participant.last_name} in {self.attendance_list.event.title}"
