###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404, HttpResponse
from django.contrib.auth.hashers import make_password

from utils.functions.generateRandomSalt import generateRandomSalt
from utils.functions.generateRandomHash import generateRandomHash
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from users.serializers import *
from kits.serializers import *

import hashlib
import secrets

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
    
    # Generate a random token of 256 bits (32 bytes)
    token_secret = secrets.token_bytes(32)

    # Concatenate the email and token
    data = email.encode() + token_secret
    
    # Calculate the SHA-256 hash
    hash_obj = hashlib.sha256(token_secret)
    hash_value = hash_obj.digest()
    
    # Convert the hash to a hexadecimal representation
    hash_hex = hash_value.hex()
    
    token = hash_hex[:32]
    token_email = hash_hex[32:]
    
    confirmation_link = str(request.get_host()) + '/api/auth/email_validation/?token={token}'.format(token=token_email)
    
    # Making data json.
    data = {
        'email': email,
        'password': password,
        'role': 'user',
        'auth': {
            'password_salt': password_salt,
            'hash_algorithm': hash_algorithm,
            'token': token,
            'email_validation_token': token_email,
        },
        'profile': {}
    }

    email_message = """
        Olá,

        Bem-vindo a Seelect! Estamos muito felizes em tê-lo conosco.

        Para confirmar o seu cadastro, clique no link abaixo:

        {link}

        Se você não se cadastrou na Seelect, por favor, ignore este e-mail.

        Estamos empolgados para tê-lo como participante do nosso evento e esperamos que você aproveite ao máximo a sua experiência na Seelect.

        Atenciosamente,
        A Equipe da Seelect
    """.format(link=confirmation_link)
    
    send_mail(
        "Confirmação de Cadastro no Seelect",
        email_message,
        "joelkalil1@gmail.com",
        ["joelkalil1@gmail.com"],
        fail_silently=False
    )

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
    
    auth = UserAuthentication.objects.get(pk=user.auth.id)
    
    if not auth.email_validation:
        return Response("Email isn't validated!", status=status.HTTP_428_PRECONDITION_REQUIRED)
    
    password_salt = user.auth.password_salt
    password = make_password(password, salt=password_salt, hasher='default')
    
    # Checking if the password is correct
    try:
        user = User.objects.get(email=email, password=password)
    except User.DoesNotExist:
        return HttpResponse('User not found!', status=status.HTTP_404_NOT_FOUND)
    
    auth.refresh_token()
    
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
# .../user/login/
@api_view(['GET'])
def email_validation(request):
    """
    Validate email.
    """
    # Getting token
    token = request.GET.get('token', None)

    # Checking if the user exist
    try:
        user = UserAuthentication.objects.get(email_validation_token=token)
    except UserAuthentication.DoesNotExist:
        raise Http404
        
    user.email_validation = True
    user.save()

    # Returning the json data of the user
    return Response("That's OK BRO, ENJOY SEELECT!")

###########################################################################################