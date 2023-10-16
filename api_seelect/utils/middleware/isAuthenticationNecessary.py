# List of all endpoints, which aren't necessary to authenticate
endpoints_with_no_authentication_necessary = [
    ('POST', '/api/auth/register/'),
    ('POST', '/api/auth/login/'),
    ('POST', '/api/contact/'),
    ('GET', '/api/events/')
]

# Function to check it
def is_authentication_necessary(request):
    if (request.method, request.path) in endpoints_with_no_authentication_necessary:
        return False
    else:
        return True