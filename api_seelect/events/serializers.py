###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import serializers
from events.models import Places, Events, EventsPlaces

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
        fields = ['id', 'title', 'category', 'number_of_inscriptions', 'max_number_of_inscriptions', 'date_created', 'place']

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