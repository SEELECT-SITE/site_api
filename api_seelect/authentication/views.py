###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404, HttpResponse
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
# .../auth/register
class Register(APIView, StandardUserSetPagination):
    """
    Register a new user.
    """
    def post(self, request, format=None):
        # Getting user data.
        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('gender', None)        

        # Creating hash and salt
        password_salt = generateRandomSalt()
        password = make_password(request.POST.get('password', None), salt=password_salt, hasher='default')

        # Defining Hash Algorithm
        hash_algorithm = 'pbkdf2_sha256'

        #
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
# .../user/login/
@api_view(['POST'])
def login(request):
    """
    Validate the username and password, to log in the user.
    """
    # Getting username and password
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    # Checking if the user exist
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    
    password_salt = user.auth.password_salt
    password = make_password(password, salt=password_salt, hasher='default')
    
    # Checking if the password is correct
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return HttpResponse('401 Unauthorized', status=401)
    
    token = UserAuthentication.objects.get(pk=user.auth.id).refresh_token()
    
    # Getting the serializer of the user
    serializer = UserSerializer(user)
    # Returning the json data of the user
    return Response(serializer.data)