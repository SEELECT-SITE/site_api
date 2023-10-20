# List of all endpoints, which aren't necessary to authenticate
endpoints_with_no_authentication_necessary = [
    ('POST', '/api/auth/register/'),
    ('POST', '/api/auth/login/'),
    ('GET', '/api/auth/email_validation/'),
    ('POST', '/api/contact/'),
    ('GET', '/api/events/'),
    ('GET', '/api/kits/models/'),
]

# Function to check it
def isAuthenticationNecessary(request):
    if (request.method, request.path) in endpoints_with_no_authentication_necessary:
        return False
    else:
        return True