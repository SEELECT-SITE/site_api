###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from functions.generateRandomSalt import generateRandomSalt
from functions.generateRandomHash import generateRandomHash

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from users.serializers import *

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


    def post(self, request, format=None):
        # Getting user data.
        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
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
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'auth': {
                'password_salt': password_salt,
                'hash_algorithm': hash_algorithm,
                'token': token,
            },
        }

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###########################################################################################
# .../user/<id>/
class UserDetail(APIView):
    """
    Retrieve, update or delete an user instance.
    """
    def get_object(self, pk):
        # Getting the user by id.
        try:
            return User.objects.get(pk=pk)
        # Return 404 if the user don't exist.
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)

        # Getting user data.
        username = request.data.get('username', user.username)
        first_name = request.data.get('first_name', user.first_name)
        last_name = request.data.get('last_name', user.last_name)
        email = request.data.get('email', user.email)
        password = request.data.get('password', user.password)        

        # Creating hash and salt
        password_salt = UserAuthentication.objects.get(pk=user.auth.id).password_salt
        password = make_password(request.data.get('password', user.password),salt=password_salt, hasher='default')

        # Generating Token
        token = generateRandomHash()

        # Making data json.
        data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'auth': {
                'token': token,
            },
        }

        serializer = UserSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

###########################################################################################