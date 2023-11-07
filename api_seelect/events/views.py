###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404, HttpResponse

from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from events.serializers import *
from kits.serializers import KitsEventsSerializer, KitsEvents
from users.serializers import UserProfileSerializer, User

from utils.functions.generateAttendanceSheet import generate_attendance_sheet

import csv

###########################################################################################
# Pagination Classes                                                                      #
###########################################################################################    
class StandardEventSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000

###########################################################################################
# Requests Classes                                                                        #
###########################################################################################
# .../api/events/
class EventsList(APIView, StandardEventSetPagination):
    """
    List all events, or create a new event.
    """
    pagination_class = StandardEventSetPagination

    def get(self, request, format=None):    
        queryset = Events.objects.get_queryset().order_by('id')
        
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = EventsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = Events(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        events_data = request.data.copy()
        places_data = events_data.pop('place', [])
        serializer = EventsSerializer(data=events_data)
        if serializer.is_valid():
            event = serializer.save()

            for place_id in places_data:
                try:
                    place = Places.objects.get(pk=place_id)
                    EventsPlaces.objects.create(event=event, place=place)
                except Places.DoesNotExist:
                    pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###########################################################################################
# .../api/events/<id>
class EventsDetail(APIView):
    """
    Retrieve, update or delete an event instance.
    """
    def get_object(self, pk):
        # Getting the event by id.
        try:
            return Events.objects.get(pk=pk)
        # Return 404 if the event don't exist.
        except Events.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        
        query = KitsEvents.objects.all().filter(event=pk)
        
        # Creating array
        participants = []
        
        # Getting all kits that are related with this event
        for element in KitsEventsSerializer(query, many=True).data:
            
            kit = Kits.objects.get(pk=element['kit'])            
            
            profile_serializer = UserProfileResumedSerializer(kit.user)
            
            participants.append(profile_serializer.data)
            
        serializer = EventsSerializer(event)
        
        # Add participants kits in event serializer
        data = serializer.data
        data['participants'] = participants
        
        return Response(data)
    
    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        
        events_data = request.data.copy()
        places_data = events_data.pop('place', None)

        event_serializer = EventsSerializer(event, data=events_data)

        if event_serializer.is_valid():
            event = event_serializer.save() # Update event data

            if not places_data == None:
                # Remove existing associations with places
                event.place.clear()

                for place_id in places_data:
                    try:
                        place = Places.objects.get(pk=place_id)
                        EventsPlaces.objects.create(event=event, place=place)
                    except Places.DoesNotExist:
                        pass
                
            return Response(event_serializer.data, status=status.HTTP_200_OK)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
###########################################################################################
# .../api/events/places/
class PlacesList(APIView, StandardEventSetPagination):
    """
    List all places, or create a new place.
    """
    pagination_class = StandardEventSetPagination

    def get(self, request, format=None):    
        queryset = Places.objects.get_queryset().order_by('id')
        
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = PlacesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = Places(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PlacesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###########################################################################################
# .../api/events/places/<id>/
class PlacesDetail(APIView):
    """
    Retrieve, update or delete a place instance.
    """
    def get_object(self, pk):
        # Getting the place by id.
        try:
            return Places.objects.get(pk=pk)
        # Return 404 if the place don't exist.
        except Places.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = PlacesSerializer(place)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = PlacesSerializer(place, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        place = self.get_object(pk)
        place.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

###########################################################################################
# .../api/events/<id>/participants/
@api_view(['GET'])
def get_participants_list(request, pk):
    """
    Get participants list by event.
    """
    
    query = KitsEvents.objects.all().filter(event=pk)
    
    # Creating array with labels    
    participants = []
    
    # Getting all kits that are related with this event
    for element in KitsEventsSerializer(query, many=True).data:
        
        kit = Kits.objects.get(pk=element['kit'])            
        
        profile_serializer = UserProfileSerializer(kit.user)
        user = User.objects.get(pk=kit.user.id)
        
        participants.append({
            "id": profile_serializer.data['id'],
            "email": user.email,
            "name": f"{profile_serializer.data['first_name']} {profile_serializer.data['last_name']}",
            "first_name": profile_serializer.data['first_name'],
            "last_name": profile_serializer.data['last_name'],
            "ies": profile_serializer.data['ies'],
            "birthday": profile_serializer.data['birthday'],
            "course": profile_serializer.data['course'],
            "semester": profile_serializer.data['semester'],
            #"kit_model": kit.model.model,
            #"kit_status": kit.is_payed
        })
        
    # Create a CSV file in memory
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participants_event_{pk}.csv"'.format(pk=pk)

    # Create the CSV writer
    writer = csv.writer(response)
    writer.writerow(['Id', 'Email', 'Name', 'First Name', 'Last Name', 'IES', 'Birthday', 'Course', 'Semester'])#, 'Kit Model', 'Payment Status']) # Headers

    # Write user data to CSV
    for participant in participants:
        writer.writerow([participant["id"], 
                        participant["email"], 
                        participant["name"], 
                        participant["first_name"],
                        participant["last_name"],
                        participant["ies"],
                        participant["birthday"],
                        participant["course"],
                        participant["semester"],
                        #participant["kit_model"], 
                        #participant["kit_status"]
        ])

    return response
    
###########################################################################################
# .../api/events/<id>/participants/pdf/
@api_view(['GET'])
def get_participants_list_pdf(request, pk):
    """
    Get participants list by event.
    """
    
    query = KitsEvents.objects.all().filter(event=pk)
    
    # Creating array    
    participants = []
    
    # Getting all kits that are related with this event
    for element in KitsEventsSerializer(query, many=True).data:
        
        kit = Kits.objects.get(pk=element['kit'])            
        
        profile_serializer = UserProfileResumedSerializer(kit.user)
        user = User.objects.get(pk=kit.user.id)
        
        participants.append({
            "id": profile_serializer.data['id'],
            "name": profile_serializer.data['name'],
            "email": user.email,
            "kit_model": kit.model.model,
            "kit_status": kit.is_payed
        })
        
    # Getting event object
    try:
        event = Events.objects.get(pk=pk)
    # Return 404 if the event don't exist.
    except Events.DoesNotExist:
        raise Http404
    
    # Returning attendance sheet
    return generate_attendance_sheet(participants, event)
    
###########################################################################################