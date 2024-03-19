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
    return render(request, 'profile.html')


def create_key(request):
    from crypto import rsa
    from core.models import PublicKey

    public_key, private_key = rsa.generate_keypair()

    #save key
    rsa.save_private_key(request.user.username, private_key)

    pbkey = PublicKey.objects.filter(user=request.user)

    if pbkey:
        pbkey.update(key=rsa.public_key_to_string(public_key))
    else:
        PublicKey.objects.create(key=rsa.public_key_to_string(public_key), user=request.user)

    return redirect('profile')
