from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from website.forms import *
from website.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def bid(request):
    return render(request, 'bid.html')

def register_page(request):
    if request.method == 'POST':
        print("Post Request")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("Valid Form")
            user = User(
                username = form.cleaned_data['username'], 
                password = form.cleaned_data['password1'],
                email = form.cleaned_data['email'],
                balance = 0.0,
                firstname = form.cleaned_data['firstname'],
                lastname = form.cleaned_data['lastname'],
                cellphone = form.cleaned_data['cellphone'],
                address = form.cleaned_data['address'],
                town = form.cleaned_data['town'],
                post_code = form.cleaned_data['postcode'],
                country = form.cleaned_data['country'] 
            )
            user.save()
            print("Write form to database")
            return render(request, 'index.html')
    form = RegistrationForm()
    return render(request, 'index.html', {'form': form})