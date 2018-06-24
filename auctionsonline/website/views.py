from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from website.forms import *
from website.models import User, Product, Auction
from datetime import datetime

# Create your views here.
def index(request):
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')    
    return render(request, 'index.html', {'auctions': auctions})

def register(request):
    return render(request, 'register.html')

def profile(request):
    return render(request, 'profile.html')

def filter_auctions(request, category):
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')    
    
    if category == "laptops":
        lap_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="LAP"
            ).order_by('time_starting')
        
        return render(request, 'index.html', {'auctions': lap_auctions})
    elif category == "consoles":
        con_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="CON"
            ).order_by('time_starting')
        
        return render(request, 'index.html', {'auctions': con_auctions})
    elif category == "games":
        gam_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="GAM"
            ).order_by('time_starting')
        
        return render(request, 'index.html', {'auctions': gam_auctions})
    elif category == "gadgets":
        gad_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="GAD"
            ).order_by('time_starting')
        
        return render(request, 'index.html', {'auctions': gad_auctions})
    elif category == "tvs":
        tel_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="TEL"
            ).order_by('time_starting')
        
        return render(request, 'index.html', {'auctions': tel_auctions})
    
    return render(request, 'index.html', {'auctions': auctions})

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
            auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')    
            return render(request, 'index.html', {'auctions': auctions})
    form = RegistrationForm()
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')    
    return render(request, 'index.html', {'form': form}, {'auctions': auctions})

def login_page(request):
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')
    if request.method == 'POST':
        print("Post Request")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("Valid Form")
            user = User.objects.filter(username=form.cleaned_data['username'])
            print(user)
            # call validation function from validation.py (password matching)
            request.session['username'] = user[0].username
            return render(request, 'index.html', {'auctions': auctions})
    return render(request, 'index.html', {'auctions': auctions})

def logout_page(request):
    try:
        del request.session['username']
    except:
        pass
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')
    return render(request, 'index.html', {'auctions': auctions})