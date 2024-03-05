from core.models import Profile
from django.contrib.auth import get_user


def profile(request):
    user = get_user(request)
    if user.is_authenticated:
        print(Profile.objects.get(user_id=user.id).birthday)
        return {'profile': Profile.objects.get(user_id=user.id)}
    else:
        return {'profile': None}