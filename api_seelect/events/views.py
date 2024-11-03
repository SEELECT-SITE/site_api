###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import Http404, HttpResponse

from datetime import datetime, timezone
from django.utils.dateparse import parse_datetime

from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from kits.models import Kits, KitsEvents
from users.models import User, UserProfile

from events.serializers import *
from kits.serializers import KitsEventsSerializer
from users.serializers import UserProfileSerializer, UserProfileResumedSerializer

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
# .../api/events/<id>/attendance/
class EventAttendanceView(APIView):
    """
    Retrieve or update the attendance list for an event.
    """
    def get_event(self, pk):
        try:
            return Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_event(pk)
        attendance_list, created = AttendanceList.objects.get_or_create(event=event)

        # Process event dates to get hours per day
        date_dict = event.date  # This is the JSONField with the date data
        hours_per_day = []
        num_days = len(date_dict)
        for day_index in range(num_days):
            day_info = date_dict.get(str(day_index), {})
            start_time_str = day_info.get('start')
            end_time_str = day_info.get('end')
            if start_time_str and end_time_str:
                # Parse the time strings into datetime objects
                start_time = parse_datetime(start_time_str)
                end_time = parse_datetime(end_time_str)
                # Ensure timezones are aware
                if start_time.tzinfo is None:
                    start_time = start_time.replace(tzinfo=timezone.utc)
                if end_time.tzinfo is None:
                    end_time = end_time.replace(tzinfo=timezone.utc)
                # Calculate the duration in hours
                duration = (end_time - start_time).total_seconds() / 3600
                hours_per_day.append(duration)
            else:
                hours_per_day.append(0)

        # Initialize days as list of False
        days = [False] * num_days

        # Get current participants of the event
        participants = self.get_event_participants(event)

        # Get existing participant IDs in the attendance list
        existing_participant_ids = set(attendance.participant.id for attendance in attendance_list.attendances.all())

        # Identify new participants who need attendance records
        new_participants = [participant for participant in participants if participant.id not in existing_participant_ids]

        # Create attendance records for new participants
        for participant in new_participants:
            Attendance.objects.create(
                attendance_list=attendance_list,
                participant=participant,
                days=days,
                hours_per_day=hours_per_day
            )

        serializer = AttendanceListSerializer(attendance_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        event = self.get_event(pk)
        attendance_list = AttendanceList.objects.get(event=event)
        serializer = AttendanceListSerializer(attendance_list, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete the attendance list for an event.
        """
        event = self.get_event(pk)
        try:
            attendance_list = AttendanceList.objects.get(event=event)
            attendance_list.delete()
            return Response({'detail': 'Attendance list deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except AttendanceList.DoesNotExist:
            return Response({'detail': 'Attendance list does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def get_event_participants(self, event):
        """
        Get participants associated with the event.
        """
        kits_events = KitsEvents.objects.filter(event=event)
        kits = [kits_event.kit for kits_event in kits_events]
        participants = UserProfile.objects.filter(kits__in=kits).distinct()
        return participants