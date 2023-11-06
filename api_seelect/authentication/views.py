###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404, HttpResponse
from django.contrib.auth.hashers import make_password

from utils.functions.generateRandomSalt import generate_random_salt
from utils.functions.generateRandomPassword import generate_random_password
from utils.functions.getEmailMessage import get_email_message, get_forget_password_message
from utils.functions.emailValidationPage import email_validation_page
from utils.middleware.getUserFromToken import get_user_from_token


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
# Requests Classes                                                                        #
###########################################################################################
# .../auth/register
@api_view(['POST'])
def register(request):
    """
    Register a new user.
    """
    # Getting email
    email = request.POST.get('email', None)    

    # Creating salt for the user password
    password_salt = generate_random_salt()
    
    # Getting password and checking if is null
    password = request.POST.get('password', None)
    if not password:
        return Response("Password can't be null!", status=status.HTTP_400_BAD_REQUEST)
    
    # Apllying hashing algorithm in password
    password = make_password(password, salt=password_salt, hasher='default')

    # Defining Hash Algorithm
    hash_algorithm = 'pbkdf2_sha256'
    
    # Generate a random token of 256 bits (32 bytes)
    token_secret = secrets.token_bytes(32)

    # Concatenate the email and token
    #token_secret = email.encode() + token_secret
    
    # Calculate the SHA-256 hash
    hash_obj = hashlib.sha256(token_secret)
    hash_value = hash_obj.digest()
    
    # Convert the hash to a hexadecimal representation
    hash_hex = hash_value.hex()
    
    # Breaking the 256 bits hash into 2 hashs of 128 bits
    token = hash_hex[:32]
    token_email = hash_hex[32:]
    
    # Creating the confirmation link to validate the email
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

    serializer = UserSerializer(data=data)

    # If the serialzier is valid
    if serializer.is_valid():
        serializer.save()
        
        # Get email message
        email_message = get_email_message(confirmation_link)
        
        # Sending email
        send_mail(
            "Confirmação de Cadastro no SEELECT",
            email_message,
            "seelect2023@gmail.com",
            [email],
            fail_silently=False
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
###########################################################################################
# .../auth/login/
@api_view(['POST'])
def login(request):
    """
    Validate the username and password, to log in the user.
    """
    # Getting email and password
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    # Checking if the user exist
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Http404
    
    # Checking if the email was validated
    if not user.auth.email_validation:
        return Response("Email isn't validated!", status=status.HTTP_428_PRECONDITION_REQUIRED)
    
    # Hashing the password
    password_salt = user.auth.password_salt
    password = make_password(password, salt=password_salt, hasher='default')
    
    # Checking if the password is correct
    if not password == user.password:
        return HttpResponse('Password Incorrect!', status=status.HTTP_404_NOT_FOUND)
    
    # Refreshing token
    user.auth.refresh_token()
    
    # Getting the serializer of the user
    serializer = UserSerializer(user)
    data = serializer.data

    # Getting the kit by the user id
    try:
        kit = Kits.objects.get(user=user.id)
    # Setting None if the kit don't exist
    except Kits.DoesNotExist:
        kit = None

    # If the kit exist, we add this on the data json
    if kit:
        kit_serializer = KitsSerializer(kit)
        # Adding kit to data json
        data['profile']['kit'] = kit_serializer.data
    
    # Returning the json data of the user
    return Response(data)

###########################################################################################
# .../auth/email_validation/
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
    
    # We set true the email validation
    user.email_validation = True
    user.save()

    # Rendering the confimation message
    html_content = email_validation_page()
    
    return HttpResponse(html_content)

###########################################################################################
# .../auth/forget_password/
@api_view(['POST'])
def forget_password(request):
    """
    Reset password to a random value.
    """
    
    # Getting email
    email = request.POST.get('email', None)
    
    # Getting user
    try: 
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response("Email not found!", status=status.HTTP_404_NOT_FOUND)
        
    # Generating random password
    password = generate_random_password(12)
    
    # Creating email message
    email_message = get_forget_password_message(password)
    
    # Encrypting the new password with the salt
    password = make_password(password, salt=user.auth.password_salt, hasher='default')

    # Updating password
    user.password = password
    user.save()
    
    # Sending email
    send_mail(
        "Confirmação de Cadastro no SEELECT",
        email_message,
        "seelect2023@gmail.com",
        [email],
        fail_silently=False
    )

    return Response("Password updated successfully!", status=status.HTTP_200_OK)

###########################################################################################
# .../auth/change_password/
@api_view(['POST'])
def change_password(request):
    """
    Change password.
    """
    
    # Getting user
    user = get_user_from_token(request)
    
    # Getting new password
    password = request.POST.get('new_password', None)
        
    # If the password is None, return error.
    if password == None:
        return Response("Password can't be null!", status=status.HTTP_400_BAD_REQUEST)
    
    # Encrypting the new password with the salt
    password = make_password(password, salt=user.auth.password_salt, hasher='default')
    
    # Updating password
    user.password = password
    user.save()

    return Response("Password updated successfully!", status=status.HTTP_200_OK)

###########################################################################################
# .../auth/change_role/
@api_view(['POST'])
def change_role(request):
    """
    Change role.
    """
    
    email = request.POST.get('email', None)
    role = request.POST.get('new_role', None)
    
    # Getting user by email
    user = User.objects.get(email=email)
        
    # If the role is user, staff or admin
    if role in ['user', 'staff', 'admin']:
        # Updating role
        user.role = role
        user.save()

        return Response("Role updated successfully!", status=status.HTTP_200_OK)
    
    # Return error
    else:
        return Response("Role can't be null!", status=status.HTTP_400_BAD_REQUEST)

###########################################################################################