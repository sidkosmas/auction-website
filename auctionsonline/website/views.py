from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from website.forms import *
from website.validation import *
from website.models import User, Product, Auction, Watchlist
from datetime import datetime

from itertools import chain

def index(request):
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')
    
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            return render(request, 'index.html', {'auctions': auctions, 'user': user[0]})
    except KeyError:
        return render(request, 'index.html', {'auctions': auctions})
    
    return render(request, 'index.html', {'auctions': auctions})

def register(request):
    return render(request, 'register.html')

def watchlist(request, auction_id):
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            auction = Auction.objects.filter(id=auction_id)
            watchlist_item = Watchlist()
            watchlist_item.auction_id = auction[0]
            watchlist_item.user_id = user[0]
            watchlist_item.save()
            
            return index(request)
    except KeyError:
        return index(request)
     
    return index(request)

def watchlist_page(request):
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            w = Watchlist.objects.filter(user_id=user[0])
            
            auctions = Auction.objects.none()
            for item in w:
                a = Auction.objects.filter(id=item.auction_id.id)
                auctions = list(chain(auctions, a))
            print(auctions)
            return render(request, 'index.html', {'auctions': auctions, 'user': user[0]})
    except KeyError:
        return index(request)

def balance(request):
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            return render(request, 'balance.html', {'user': user[0]})
    except KeyError:
        return index(request)
        
    return index(request)

def topup(request):
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            try:
                if request.session['username']:
                    user = User.objects.get(username=request.session['username'])
                    user.balance += form.cleaned_data['amount']
                    user.save()
            except KeyError:
                return index(request)
    
    return index(request)

def filter_auctions(request, category):    
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
    
    return index(request)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
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
    return index(request)

def login_page(request):
    if request.method == 'POST':
        print("Post Request")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("Valid Form")
            is_valid=validate_login(form.cleaned_data['username'], form.cleaned_data['password'])
            if is_valid :
                request.session['username'] = form.cleaned_data['username']
    return index(request)

def logout_page(request):
    try:
        del request.session['username']
    except:
        pass
    return index(request)