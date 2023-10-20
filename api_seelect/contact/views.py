###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404

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
    List all contacts, or create a new contact.
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
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###########################################################################################
# .../api/contact/<id>/
class ContactDetail(APIView):
    """
    Retrieve, update or delete an contact instance.
    """
    def get_object(self, pk):
        # Getting the event by id.
        try:
            return Contact.objects.get(pk=pk)
        # Return 404 if the event don't exist.
        except Contact.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        contact = self.get_object(pk)

        serializer = ContactSerializer(contact, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        contact = self.get_object(pk)
        contact.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
###########################################################################################