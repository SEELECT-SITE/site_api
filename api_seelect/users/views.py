###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404
from django.contrib.auth.hashers import make_password

from utils.functions.generateRandomSalt import generateRandomSalt
from utils.functions.generateRandomHash import generateRandomHash

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from users.serializers import *
from kits.serializers import *


###########################################################################################
# Pagination Classes                                                                      #
###########################################################################################
class StandardUserSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

###########################################################################################
# Requests Classes                                                                        #
###########################################################################################
# .../api/<str:role>/
class RoleList(APIView, StandardUserSetPagination):
    """
    List all users from a role, or create a new user from that role.
    """
    pagination_class = StandardUserSetPagination
    
    def get(self, request, role, format=None):
        queryset = User.objects.get_queryset().order_by('id')

        if role in ['user', 'staff', 'admin']:
            queryset = queryset.filter(role=role)
        else:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = User(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, role, format=None):
        # Getting user data.
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)        

        # Creating hash and salt
        password_salt = generateRandomSalt()
        password = make_password(request.POST.get('password', None),salt=password_salt, hasher='default')

        # Defining Hash Algorithm
        hash_algorithm = 'pbkdf2_sha256'

        # Generating Token
        token = generateRandomHash()

        # Making data json.
        data = {
            'role': role,
            'email': email,
            'password': password,
            'auth': {
                'password_salt': password_salt,
                'hash_algorithm': hash_algorithm,
                'token': token,
            },
            'profile': {}
        }

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###########################################################################################
# .../api/<str:role>/<int:id>/
class RoleDetail(APIView):
    """
    Retrieve, update or delete an user instance.
    """
    def get_object(self, role, pk):
        # Getting the user by id.
        try:
            return User.objects.get(pk=pk, role=role)
        # Return 404 if the user don't exist.
        except User.DoesNotExist:
            raise Http404
        
    def get_kit(self, pk):
        # Getting the kit by the user id.
        try:
            return Kits.objects.get(user=pk)
        # Return None if the user don't exist.
        except Kits.DoesNotExist:
            return None

    def get(self, request, role, pk, format=None):
        user = self.get_object(role, pk)
        serializer = UserSerializer(user)
        data = serializer.data

        # Checking if has some kit to add in the JSON
        kit = self.get_kit(pk)
        if kit:
            kit_serializer = KitsSerializer(kit)
            # Adding kit info
            data['profile']['kit'] = kit_serializer.data
        
        return Response(data)

    def put(self, request, role, pk, format=None):
        user = self.get_object(role, pk)

        # Getting user data.
        email = request.data.get('email', user.email)
        password = request.data.get('password', user.password)        

        # Creating hash and salt
        password_salt = UserAuthentication.objects.get(pk=user.auth.id).password_salt
        password = make_password(request.data.get('password', user.password),salt=password_salt, hasher='default')

        # Defining Hash Algorithm
        hash_algorithm = 'pbkdf2_sha256'

        # Generating Token
        token = generateRandomHash()

        profile = UserProfileSerializer(user.profile)

        # Making data json.
        data = {
            'role': role,
            'email': email,
            'password': password,
            'auth': {
                'password_salt': password_salt,
                'hash_algorithm': hash_algorithm,
                'token': token,
            },
            'profile': profile.data,
        }

        serializer = UserSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, role, pk, format=None):
        user = self.get_object(role, pk)
        user.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

###########################################################################################
# .../api/<str:role>/profile/<int:id>/
class UserProfileDetail(APIView, StandardUserSetPagination):
    """
    Retrieve or update an user profile instance.
    """
    def get_object(self, pk):
        # Getting the user by id.
        try:
            return UserProfile.objects.get(pk=pk)
        # Return 404 if the user don't exist.
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, role, pk, format=None):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, role, pk, format=None):
        profile = self.get_object(pk)     

        serializer = UserProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
###########################################################################################
# .../users/
class UserList(APIView, StandardUserSetPagination):
    """
    List all users, or create a new user.
    """
    pagination_class = StandardUserSetPagination

    def get(self, request, format=None):
        queryset = User.objects.get_queryset().order_by('id')

        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = User(queryset, many=True)
        return Response(serializer.data)

###########################################################################################