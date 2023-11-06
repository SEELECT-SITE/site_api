###########################################################################################
# Imports                                                                                 #
###########################################################################################
from rest_framework import status

from django.http import HttpResponse

from utils.middleware.getUserFromToken import get_user_from_token
from utils.middleware.isAuthenticationNecessary import isAuthenticationNecessary
from utils.middleware.userAuthentication import canUserAcess

###########################################################################################
# Middleware                                                                              #
###########################################################################################
# Authentication Middleware
class AuthenticationMiddleware:
    # Init default
    def __init__(self, get_response):
        self.get_response = get_response

    # Call default
    def __call__(self, request):
        # Endpoints with is not necessary the token
        if not isAuthenticationNecessary(request):
            response = self.get_response(request)
            return response
        
        # If the endpoint is not there, let's check the Authorization Token
        # Gettin user from token
        user = get_user_from_token(request)
        
        # Checking if we got some user
        if user is None:
            return HttpResponse("Invalid token", status=status.HTTP_401_UNAUTHORIZED)
        
        # Now, let's check if the user can acess this endpoint
        if user.role == 'user' and canUserAcess(request=request, user=user) == False:
            # Returning status 401
            return HttpResponse("Access unauthorized!", status=status.HTTP_401_UNAUTHORIZED)

        # If the token is valid, go to request
        response = self.get_response(request)
        return response

###########################################################################################