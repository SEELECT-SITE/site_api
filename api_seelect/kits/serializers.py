###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import serializers
from kits.models import *
from events.serializers import EventsSerializer

###########################################################################################
# Serializers                                                                             #
############################################################################################
# Kits Model Serializer
class KitsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = KitModels
        fields = '__all__'
        
###########################################################################################
# Kits Serializer
class KitsSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    model_detail = KitsModelSerializer(source='model', read_only=True)

    class Meta:
        model = Kits
        ordering = ['id']
        fields = ['id', 'user', 'discount', 'is_payed', 'model', 'model_detail', 'events', 'date_created']

    def get_events(self, obj):
        # Assuming you have a ManyToMany relationship to Minicourses in Events
        events = obj.events.all()                           # Retrieve the associated mini_courses
        return EventsSerializer(events, many=True).data     # Serialize the mini_courses 

###########################################################################################
# KitsEvents Serializer
class KitsEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitsEvents
        fields = '__all__'

###########################################################################################
# KitsDiscount Serializer
class KitsDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitsDiscount
        fields = '__all__'

###########################################################################################