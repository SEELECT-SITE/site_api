###########################################################################################
# Imports                                                                                 #
###########################################################################################
from users.models import User, UserAuthentication

###########################################################################################
# Functions                                                                               #
###########################################################################################
def get_user_from_token(request):
    # Getting token from headers
    try:
        token = request.headers['Token']
    except:
        token = None
    
    # Checking if the token exist
    if token:
        try:
            id = UserAuthentication.objects.get(token=token).id
            user = User.objects.get(pk=id)
            # Returning the user
            return user
        except:
            pass
        
    # Returning None if has no Token or no user for this Token
    return None

###########################################################################################