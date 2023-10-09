from users.models import User, UserAuthentication

def get_user_from_token(request):
    try:
        token = request.headers['Token']
    except:
        token = None
    if token:
        try:
            id = UserAuthentication.objects.get(token=token).id
            user = User.objects.get(pk=id)
            return user
        except:
            pass
    return None