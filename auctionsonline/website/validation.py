from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def validate_login(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        return True
    else:
        return False

def validate_registration(username, password1, password2, email):
    user = User.objects.filter(username=username)

    if user:
        print('User already exists')
        return False
    if password1 != password2:
        return False
    email = User.objects.filter(email=email)
    if email:
        print('Email already exists')
        return False

    return True
