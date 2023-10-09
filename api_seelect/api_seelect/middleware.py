from users.serializers import *

from rest_framework import status

from django.http import HttpResponse

from utils.middleware.getUserFromToken import get_user_from_token
from utils.middleware.isAuthenticationNecessary import is_authentication_necessary

# Token Authentication Middleware
class TokenAuthenticationMiddleware:
    # Init default
    def __init__(self, get_response):
        self.get_response = get_response

    # Call default
    def __call__(self, request):
        # Endpoints with is not necessary the token
        if not is_authentication_necessary(request):
            response = self.get_response(request)
            return response
        # Check token here
        user = get_user_from_token(request)
        if user is None:
            return HttpResponse("Invalid token", status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response