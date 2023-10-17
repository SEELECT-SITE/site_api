###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import serializers
from users.models import *

###########################################################################################
# Serializers                                                                             #
###########################################################################################
# User Account Serializer.
class UserAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthentication
        fields = ['id', 'token', 'password_salt']

###########################################################################################
# User Profile Serializer.
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'ies', 'cpf', 'birthday', 'course', 'semester']
        
###########################################################################################
# User Profile Resumed Serializer.
class UserProfileResumedSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'name']
        
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

###########################################################################################
# User Serializer, it's a nest serializer.
class UserSerializer(serializers.ModelSerializer):
    auth = UserAuthenticationSerializer(many=False)
    profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        ordering = ['id']
        fields = ['id', 'auth', 'profile', 'role', 'password', 'email', 'date_joined']

    # Making it nested with Profile and Token.
    def create(self, validated_data):
        #print(validated_data)
        # Separating data
        auth_data = validated_data.pop('auth')
        profile_data = validated_data.pop('profile')

        # Crating user object
        user = User.objects.create(**validated_data)

        # Creating others objects
        UserAuthentication.objects.create(user=user, **auth_data)
        UserProfile.objects.create(user=user, **profile_data)
        
        return user

    def update(self, instance, validated_data):
        # Separating data
        auth_data = validated_data.pop('auth')
        profile_data = validated_data.pop('profile')
        
        for key in validated_data.keys():
            setattr(instance, key, validated_data.get(key, getattr(instance, key)))
        instance.save()

        auth = instance.auth
        for key in auth_data.keys():
            setattr(auth, key, auth_data.get(key, getattr(auth, key)))
        auth.save()

        profile = instance.profile
        for key in profile_data.keys():
            setattr(profile, key, profile_data.get(key, getattr(profile, key)))
        profile.save()
        
        return instance
###########################################################################################