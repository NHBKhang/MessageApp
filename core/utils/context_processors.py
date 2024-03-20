from core.models import Profile, Notification, PublicKey
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
    try:
        key = PublicKey.objects.get(user=request.user)
    except:
        key = None

    return {'public_key': key}


def notifications(request):
    from crypto.errors import rsa_keys_check, error_message

    error = None
    try:
        notifications = Notification.objects.filter(user=request.user).order_by('-date_added')
        error = rsa_keys_check(request.user)
    except:
        notifications = None
    print(error)
    if error:
        note = notifications.filter(type=error).filter(is_read=False)
        if not note:
            content, description = error_message(error)
            Notification.objects.create(content=content, user=request.user, type=error, description=description)

    if notifications:
        return {'notifications': notifications.all(),
                'unread_count': notifications.filter(is_read=False).count()}
    else:
        return {}
