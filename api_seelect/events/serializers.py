###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import serializers
from events.models import (
    Places,
    Events,
    EventsPlaces,
    Attendance,
    AttendanceList
)
from kits.serializers import *

###########################################################################################
# Serializers                                                                             #
############################################################################################
# Places Serializer
class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = ['id', 'location', 'url_location', 'capacity', 'equipaments', 'date_created']

###########################################################################################
# Events Serializer
class EventsSerializer(serializers.ModelSerializer):
    place = serializers.SerializerMethodField()
    
    class Meta:
        model = Events
        ordering = ['id']
        fields = ['id', 'title', 'host', 'category', 'number_of_inscriptions', 'max_number_of_inscriptions', 'date', 'description', 'date_created', 'place']

    def get_place(self, obj):
        # Assuming you have a ManyToMany relationship to Places in Events
        place = obj.place.all()                            # Retrieve the associated places
        return PlacesSerializer(place, many=True).data     # Serialize the places

###########################################################################################
# EventsPlaces Serializer
class EventsPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsPlaces
        fields = '__all__'

###########################################################################################
# Attendance Serializer
class ParticipantAttendanceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='participant.id')
    name = serializers.SerializerMethodField()
    days = serializers.ListField(child=serializers.BooleanField(), default=[])
    hours_per_day = serializers.ListField(child=serializers.FloatField(), read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'name', 'days', 'hours_per_day']

    def get_name(self, obj):
        return f"{obj.participant.first_name} {obj.participant.last_name}"

    def update(self, instance, validated_data):
        instance.days = validated_data.get('days', instance.days)
        instance.save()
        return instance

###########################################################################################
# AttendanceList Serializer
class AttendanceListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='event.title', read_only=True)
    participants = ParticipantAttendanceSerializer(source='attendances', many=True)

    class Meta:
        model = AttendanceList
        fields = ['title', 'participants']

    def update(self, instance, validated_data):
        participants_data = validated_data.pop('attendances', [])
        for participant_data in participants_data:
            participant_id = participant_data['participant']['id']
            attendance_instance = instance.attendances.get(participant__id=participant_id)
            attendance_serializer = ParticipantAttendanceSerializer(
                attendance_instance, data=participant_data, partial=True
            )
            attendance_serializer.is_valid(raise_exception=True)
            attendance_serializer.save()
        return instance