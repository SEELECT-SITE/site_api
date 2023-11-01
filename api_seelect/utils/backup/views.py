###########################################################################################
# Imports                                                                                 #
###########################################################################################
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework import status

from users.models import User
from events.models import Events

import csv

###########################################################################################
# Requests Classes                                                                        #
###########################################################################################
# .../export_users
@api_view(['GET'])
def export_users(request):
    # Obter todos os usuários
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
    response['Content-Disposition'] = 'attachment; filename="events_backup.csv"'

    # Create the CSV writer
    writer = csv.writer(response)
    writer.writerow(['Title', 'Host', 'Category', 'Number of Inscriptions', 'Max Number of Inscriptions', 'Description', 'Date Created'])  # Headers

    # Write event data to CSV
    for event in events:
        writer.writerow([event.title, event.host, event.category, event.number_of_inscriptions, event.max_number_of_inscriptions, event.description, event.date_created])

    return response

###########################################################################################