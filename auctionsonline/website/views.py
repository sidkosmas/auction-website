from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from website.forms import *
from website.validation import *
from website.models import User, Product, Auction, Watchlist, Bid
from datetime import datetime, timedelta
from django.utils import timezone

def index(request):
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')
        
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            watchlist = Watchlist.objects.filter(user_id=user[0]).order_by('auction_id__time_starting')
            return render(request, 'index.html', {'auctions': auctions, 'user': user[0], 'watchlist': watchlist})
    except KeyError:
        return render(request, 'index.html', {'auctions': auctions})
    
    return render(request, 'index.html', {'auctions': auctions})

def bid_page(request, auction_id):    
    try:
        if request.session['username']:
            auction = Auction.objects.filter(id=auction_id)
            if auction[0].time_starting > timezone.now():
                return index(request)
            user = User.objects.filter(username=request.session['username'])
            
            stats = []
            time_left = auction[0].time_ending - timezone.now()
            days, seconds = time_left.days, time_left.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            time_left = str(minutes) + "m " + str(seconds) + "s"
            
            stats.append(time_left)
            current_cost = 0.20 + (auction[0].number_of_bids * 0.20)
            current_cost = "%0.2f" % current_cost
            stats.append(current_cost)
            if days < 0:
                stats.append(False)
            else:
                stats.append(True)
                
            latest_bid = Bid.objects.all().order_by('-bid_time')
            if latest_bid:
                winner = User.objects.filter(id=latest_bid[0].user_id.id)
                stats.append(winner[0].username)
            else:
                stats.append(None)
            
            return render(request, 'bid.html', {'auction': auction[0], 'user': user[0], 'stats': stats})
    except KeyError:
        return index(request)
    
    return index(request)

def raise_bid(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    if auction.time_ending < timezone.now():
        return bid_page(request, auction_id)
    elif auction.time_starting > timezone.now():
        return index(request)
        
    bid = Bid()
    try:
        if request.session['username']:
            user = User.objects.get(username=request.session['username'])
            if user.balance > 0.0:
                latest_bid = Bid.objects.all().order_by('-bid_time')
                if not latest_bid:
                    user.balance = float(user.balance) - 1.0
                    user.save()
                    bid.user_id = user
                    bid.auction_id = auction
                    bid.bid_time = timezone.now()
                    bid.save()
                    auction.number_of_bids += 1
                    auction.time_ending = timezone.now() + timedelta(minutes=5)
                    auction.save()
                else:
                    current_winner = User.objects.filter(id=latest_bid[0].user_id.id)
                    if current_winner[0].id != user.id:
                        user.balance = float(user.balance) - 1.0
                        user.save()
                        bid.user_id = user
                        bid.auction_id = auction
                        bid.bid_time = timezone.now()
                        bid.save()
                        auction.number_of_bids += 1
                        auction.time_ending = timezone.now() + timedelta(minutes=5)
                        auction.save()
                
            return bid_page(request, auction_id)
    except KeyError:
        return bid_page(request, auction_id)
    
    return bid_page(request, auction_id)

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
        form = LoginForm(request.POST)
        if form.is_valid():
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