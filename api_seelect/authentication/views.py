###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from utils.functions.generateRandomSalt import generateRandomSalt
from utils.functions.generateRandomHash import generateRandomHash

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
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
# .../auth/register
@api_view(['POST'])
def register(request):
    """
    Register a new user.
    """
    # Getting user data.
    email = request.POST.get('email', None)    

    # Creating hash and salt
    password_salt = generateRandomSalt()
    password = make_password(request.POST.get('password', None), salt=password_salt, hasher='default')

    # Defining Hash Algorithm
    hash_algorithm = 'pbkdf2_sha256'

    # Generatin Token
    token = generateRandomHash()

    # Making data json.
    data = {
        'email': email,
        'password': password,
        'role': 'user',
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
# .../user/login/
@api_view(['POST'])
def login(request):
    """
    Validate the username and password, to log in the user.
    """
    # Getting username and password
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    # Checking if the user exist
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Http404
    
    password_salt = user.auth.password_salt
    password = make_password(password, salt=password_salt, hasher='default')
    
    # Checking if the password is correct
    try:
        user = User.objects.get(email=email, password=password)
    except User.DoesNotExist:
        return HttpResponse('User not found!', status=status.HTTP_404_NOT_FOUND)
    
    UserAuthentication.objects.get(pk=user.auth.id).refresh_token()
    
    # Getting the serializer of the user
    serializer = UserSerializer(User.objects.get(pk=user.id))
    data = serializer.data

    # Getting the kit by the user id.
    try:
        kit = Kits.objects.get(user=user.id)
    # Setting None if the kit don't exist.
    except Kits.DoesNotExist:
        kit = None

    if kit:
        kit_serializer = KitsSerializer(kit)
        # Adding kit to data json
        data['profile']['kit'] = kit_serializer.data
    
    # Returning the json data of the user
    return Response(data)

###########################################################################################