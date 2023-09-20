###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import serializers
from users.models import User, UserAuthentication

###########################################################################################
# Serializers                                                                             #
###########################################################################################
# User Account Serializer.
class UserAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthentication
        fields = ['id', 'token', 'password_salt']

###########################################################################################
# User Serializer, it's a nest serializer.
class UserSerializer(serializers.ModelSerializer):
    auth = UserAuthenticationSerializer(many=False)

    class Meta:
        model = User
        ordering = ['id']
        fields = ['id', 'auth', 'first_name', 'last_name', 'password', 'email', 'date_joined']

    # Making it nested with Profile and Token.
    def create(self, validated_data):
        #print(validated_data)
        # Separating data
        auth_data = validated_data.pop('auth')
        # Crating user object
        user = User.objects.create(**validated_data)
        # Creating others objects
        UserAuthentication.objects.create(user=user, **auth_data)
        
        return user

    def update(self, instance, validated_data):
        # Separating data
        auth_data = validated_data.pop('auth')
        
        for key in validated_data.keys():
            setattr(instance, key, validated_data.get(key, getattr(instance, key)))
        instance.save()

        auth = instance.auth
        for key in auth_data.keys():
            setattr(auth, key, auth_data.get(key, getattr(auth, key)))
        auth.save()
        
        return instance
###########################################################################################