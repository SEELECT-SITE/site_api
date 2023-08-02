###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.hashers import make_password


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .serializers import *

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
# .../contact/
class ContactList(APIView, StandardUserSetPagination):
    """
    List all users, or create a new user.
    """
    pagination_class = StandardUserSetPagination

    def get(self, request, format=None):
        queryset = Contact.objects.get_queryset().order_by('id')

        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = ContactSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = Contact(queryset, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        # Getting user data.
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        message = request.POST.get('message', None)

        # Making data json.
        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
        }

        serializer = ContactSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###########################################################################################