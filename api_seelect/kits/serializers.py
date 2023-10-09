###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import serializers
from kits.models import *
from events.serializers import EventsSerializer

###########################################################################################
# Serializers                                                                             #
############################################################################################
# Kits Serializer
class KitsSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    minicourse = serializers.SerializerMethodField()
    workshops = serializers.SerializerMethodField()
    speeches = serializers.SerializerMethodField()

    class Meta:
        model = Kits
        ordering = ['id']
        fields = ['id', 'user', 'is_payed', 'model', 'events', 'minicourse', 'workshops', 'speeches', 'date_created']

    def get_events(self, obj):
        # Assuming you have a ManyToMany relationship to Minicourses in Events
        events = obj.events.all()                           # Retrieve the associated mini_courses
        return EventsSerializer(events, many=True).data     # Serialize the mini_courses 
    
    def get_minicourse(self, obj):
        minicourse = obj.events.all().filter(category='minicurso')
        return EventsSerializer(minicourse, many=True).data
    
    def get_workshops(self, obj):
        workshops = obj.events.all().filter(category='workshop')
        return EventsSerializer(workshops, many=True).data
    
    def get_speeches(self, obj):
        speeches = obj.events.all().filter(category='workshop')
        return EventsSerializer(speeches, many=True).data

###########################################################################################
# EventsPlaces Serializer
class KitsEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitsEvents
        fields = '__all__'

###########################################################################################