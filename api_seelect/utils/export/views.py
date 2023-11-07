###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework import status

from users.serializers import User, UserProfileResumedSerializer
from kits.models import Kits
from events.models import Events

import csv

###########################################################################################
# Requests Classes                                                                        #
###########################################################################################
# .../export_users
@api_view(['GET'])
def export_users(request):
    # Get all users
    users = User.objects.all()

    # Create a CSV file in memory
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_backup.csv"'

    # Create the CSV writer
    writer = csv.writer(response)
    writer.writerow(['Role', 'Email', 'Password', 'Date Joined']) # Headers

    # Write user data to CSV
    for user in users:
        writer.writerow([user.role, user.email, user.password, user.date_joined])

    return response

###########################################################################################
# .../export_events
@api_view(['GET'])
def export_events(request):
    # Get all events
    events = Events.objects.all()

    # Create a CSV file in memory
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="events.csv"'

    # Create the CSV writer
    writer = csv.writer(response)
    writer.writerow(['Id', 'Title', 'Host', 'Category', 'Number of Inscriptions', 'Max Number of Inscriptions', 'Description', 'Date Created'])  # Headers

    # Write event data to CSV
    for event in events:
        writer.writerow([event.id, event.title, event.host, event.category, event.number_of_inscriptions, event.max_number_of_inscriptions, event.description, event.date_created])

    return response

###########################################################################################
# .../export_kits
@api_view(['GET'])
def export_kits(request):
    # Get all kits
    kits = Kits.objects.all()
    
    users = [] 
    
    for kit in kits:
        
        profile_serializer = UserProfileResumedSerializer(kit.user)
        user = User.objects.get(pk=kit.user.id)
        
        users.append({
            "id": profile_serializer.data['id'],
            "name": profile_serializer.data['name'],
            "email": user.email,
            "kit_model": kit.model.model,
            "kit_status": kit.is_payed
        })
        
    # Create a CSV file in memory
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_backup.csv"'
    
    # Create the CSV writer
    writer = csv.writer(response)
    writer.writerow(['Id', 'Name', 'Email', 'Kit Model', 'Payment Status']) # Headers

    # Write user data to CSV
    for user in users:
        writer.writerow([user["id"], user["name"], user["email"], user["kit_model"], user["kit_status"]])

    return response

###########################################################################################