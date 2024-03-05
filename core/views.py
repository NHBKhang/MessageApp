from django.contrib.auth import login, get_user
from django.shortcuts import render, redirect
from .forms import SignUpForm


def frontpage(request):
    return render(request, 'core/frontpage.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})


def profile(request):
    from core.models import PublicKey

    try:
        key = PublicKey.objects.get(user_id=get_user(request).id)
    except:
        key = None

    return render(request, 'profile.html',
                  {'key': key})
