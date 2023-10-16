###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from events.serializers import *
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
# .../api/kits/
class KitsList(APIView, StandardUserSetPagination):
    """
    List all kits, or create a new kit.
    """
    pagination_class = StandardUserSetPagination

    def get(self, request, format=None):    
        queryset = Kits.objects.get_queryset().order_by('id')
        
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = KitsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = Kits(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        kits_data = request.data.copy()
        events_data = kits_data.pop('events', [])

        user_id = request.data.get('user')

        try:
            user_profile = UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile with ID {} does not exist.".format(user_id)}, status=status.HTTP_404_NOT_FOUND)

        serializer = KitsSerializer(data=kits_data)

        if serializer.is_valid():
            serializer.validated_data['user'] = user_profile
            kit = serializer.save()

            for events_id in events_data:
                try:
                    event = Events.objects.get(pk=events_id)
                    KitsEvents.objects.create(kit=kit, event=event)
                except Events.DoesNotExist:
                    pass

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

###########################################################################################
# .../api/kits/<id>
class KitsDetail(APIView):
    """
    Retrieve, update or delete an event instance.
    """
    def get_object(self, pk):
        # Getting the event by id.
        try:
            return Kits.objects.get(pk=pk)
        # Return 404 if the event don't exist.
        except Kits.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = KitsSerializer(event)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        
        kits_data = request.data.copy()
        events_data = kits_data.pop('events', [])

        kits_serializer = KitsSerializer(event, data=kits_data)

        if kits_serializer.is_valid():
            kit = kits_serializer.save() # Update event data

            # Remove existing associations with places
            kit.events.clear()

            for events_id in events_data:
                try:
                    event = Events.objects.get(pk=events_id)
                    KitsEvents.objects.create(kit=kit, event=event)
                except Events.DoesNotExist:
                    pass
            
            return Response(kits_serializer.data, status=status.HTTP_200_OK)
        return Response(kits_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        kit = self.get_object(pk)
        kit.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
###########################################################################################