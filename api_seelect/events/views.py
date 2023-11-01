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
from users.serializers import UserProfileResumedSerializer, User

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image

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
    
    # Creating array
    participants = "id,name,email\r"
    
    participants = [{
        "id": "id",
        "name": "name",
        "email": "email",
    }]
    
    # Getting all kits that are related with this event
    for element in KitsEventsSerializer(query, many=True).data:
        
        kit = Kits.objects.get(pk=element['kit'])            
        
        profile_serializer = UserProfileResumedSerializer(kit.user)
        user = User.objects.get(pk=kit.user.id)
        
        participants.append({
            "id": profile_serializer.data['id'],
            "name": profile_serializer.data['name'],
            "email": user.email
        })
    
    return Response(participants)

###########################################################################################
# .../api/events/<id>/participants/pdf/
@api_view(['GET'])
def get_participants_list_pdf(request, pk):
    """
    Get participants list by event.
    """
            
    query = KitsEvents.objects.all().filter(event=pk)
    
    # Creating array
    participants = "id,name,email\r"
    
    participants = []
    
    # Getting all kits that are related with this event
    for element in KitsEventsSerializer(query, many=True).data:
        
        kit = Kits.objects.get(pk=element['kit'])            
        
        profile_serializer = UserProfileResumedSerializer(kit.user)
        user = User.objects.get(pk=kit.user.id)
        
        participants.append({
            "id": profile_serializer.data['id'],
            "name": profile_serializer.data['name'],
            "email": user.email
        })
        
    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_sheet.pdf"'

    # Create the PDF using ReportLab
    document = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    # Getting event object
    try:
        event = Events.objects.get(pk=pk)
    # Return 404 if the event don't exist.
    except Events.DoesNotExist:
        raise Http404
    
    # Add logo above the header
    logo_path = './utils/static/img/logo.png'  # Provide the actual path to your logo
    logo = Image(logo_path, width=100, height=100)  # Adjust width and height as needed

    elements.append(logo)
    elements.append(Spacer(1, 12))  # Add some space between logo and event info
    
    # Add event information as header
    event_info = [
        (f"Attendance Sheet", "Title"),
        (f"{event.id} - {event.title}", "Heading2"),
        (f"Host: {event.host}", "Heading3"),
        (f"Category: {event.category}",  "Heading3"),
        (f"Number of Inscriptions: {event.number_of_inscriptions}",  "Heading3"),
        (f"Number of Inscriptions: {event.max_number_of_inscriptions}",  "Heading3")
    ]
    
    # Get the default styles for paragraphs
    styles = getSampleStyleSheet()
    
    for info in event_info:
        # Define a custom style with Times New Roman font
        style = ParagraphStyle(
            name='TimesNewRoman',
            fontName='Times-Roman',
            parent=styles[info[1]]
        )
        elements.append(Paragraph(info[0], style))
    elements.append(Spacer(1, 12))  # Add some space between event info and table

    
    # Create a list of lists to represent the table
    data = [["Name", "Email", "Signature"]]

    for participant in participants:
        data.append([participant["name"], participant["email"], ""])

    # Define the column widths (in points)
    col_widths = [220, 190, 150]

    # Create the table with specified column widths
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blueviolet),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Add the table to the list of elements
    elements.append(table)

    # Build the PDF
    document.build(elements)

    return response
    
###########################################################################################