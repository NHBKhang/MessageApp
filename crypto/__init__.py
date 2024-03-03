


if __name__ == '__main__':
    import os, django

    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangochat.settings'
    django.setup()

    from room.models import Room

    Room.objects.create(name="Test")