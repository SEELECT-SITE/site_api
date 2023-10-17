###########################################################################################
# Imports                                                                                 #
###########################################################################################
from kits.models import Kits

###########################################################################################
# User Endpoints Generator, based in the user id and role.
def getUserAuthenticationEndpoints(user):
    # List of all endpoints that the user can acess
    user_endpoints = []

    try:
        kit = Kits.objects.get(user=user.id)
        # /api/kits/id/
        user_endpoints.append(('GET', '/api/kits/' + str(kit.id) + '/'))
        user_endpoints.append(('PUT', '/api/kits/' + str(kit.id) + '/'))
        #user_endpoints.append(('DELETE', '/api/kits/' + str(kit.id) + '/'))
    except:
        user_endpoints.append(('POST', '/api/kits/'))
    
    # /api/users/user/id/
    user_endpoints.append(('GET', '/api/users/user/' + str(user.id) + '/'))
    user_endpoints.append(('PUT', '/api/users/user/' + str(user.id) + '/'))
    #user_endpoints.append(('DELETE', '/api/users/user/' + str(user.id) + '/'))
    
    # /api/users/user/id/profile/
    user_endpoints.append(('GET', '/api/users/user/' + str(user.id) + '/profile/'))
    user_endpoints.append(('PUT', '/api/users/user/' + str(user.id) + '/profile/'))

    return user_endpoints
    
###########################################################################################
# Function to check if the endpoint is on the list
def canUserAcess(request, user):
    if (request.method, request.path) in getUserAuthenticationEndpoints(user=user):
        return True
    else:
        return False
    
###########################################################################################