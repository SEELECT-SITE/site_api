###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import serializers
from authentication.models import HashingAlgorithm

###########################################################################################
# Serializers                                                                             #
###########################################################################################
# User Account Serializer.
class HashingAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashingAlgorithm
        fields = ['id', 'algorithm_name']