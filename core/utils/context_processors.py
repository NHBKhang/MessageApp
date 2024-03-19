from core.models import Profile
from django.contrib.auth import get_user
from django.db import connection


def profile(request):
    user = get_user(request)

    if user.is_authenticated:
        try:
            p = Profile.objects.get(user_id=user.id)
        except:
            import datetime
            p = Profile.objects.create(user_id=user.id, birthday=datetime.datetime.now(),
                                       avatar='https://cdn-icons-png.flaticon.com/512/3541/3541871.png')

        return {'profile': p}
    else:
        return {'profile': None}


def public_key(request):
    from core.models import PublicKey

    try:
        key = PublicKey.objects.get(user=request.user)
    except:
        key = None

    return {'public_key': key}
