from django.contrib.auth.models import User
from django.shortcuts import render

from django.utils import timezone
from datetime import datetime
from itertools import chain

from website.forms import *
from website.models import Product, Auction, Watchlist, Bid, Chat, UserDetails

from website.validation import validate_login, validate_registration
from website.transactions import increase_bid, remaining_time

def index(request):
    """
    The main page of the website

    Returns
    -------
    HTTPResponse
        The index page with the current and future auctions.
    """
    auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')

    try:
        if request.session['username']:
            user = User.objects.get(username=request.session['username'])

            w = Watchlist.objects.filter(user_id=user)
            watchlist = Auction.objects.none()
            for item in w:
                a = Auction.objects.filter(id=item.auction_id.id)
                watchlist = list(chain(watchlist, a))

            userDetails = UserDetails.objects.get(user_id=user.id)
            return render(request, 'index.html',
                {'auctions': auctions, 'balance': userDetails.balance, 'watchlist': watchlist})
    except KeyError:
        return render(request, 'index.html', {'auctions': auctions})

    return render(request, 'index.html', {'auctions': auctions})

def bid_page(request, auction_id):
    """
    Returns the bid page for the
    selected auction.

    Parametes
    ---------
    auction_id : class 'int'

    Returns
    -------
    HTTPResponse
        Return the bidding page for the selected auction.
    Function : index(request)
        If the user is not logged in.
    """
    print(type(auction_id))
    try:
        # if not logged in return to the index page.
        if request.session['username']:
            # If the auction hasn't started return to the index page.
            auction = Auction.objects.filter(id=auction_id)
            if auction[0].time_starting > timezone.now():
                return index(request)
            user = User.objects.filter(username=request.session['username'])

            stats = []
            time_left, expired = remaining_time(auction[0])
            stats.append(time_left) # First element in stats list

            current_cost = 0.20 + (auction[0].number_of_bids * 0.20)
            current_cost = "%0.2f" % current_cost
            stats.append(current_cost)

            # Second element in stats list
            if expired < 0: # if auction ended append false.
                stats.append(False)
            else:
                stats.append(True)

            # Third element in stats list
            latest_bid = Bid.objects.all().order_by('-bid_time')
            if latest_bid:
                winner = User.objects.filter(id=latest_bid[0].user_id.id)
                stats.append(winner[0].username)
            else:
                stats.append(None)

            # Fourth element in stats list
            chat = Chat.objects.all().order_by('time_sent')
            stats.append(chat)

            # Getting user's watchlist.
            w = Watchlist.objects.filter(user_id=user[0])
            watchlist = Auction.objects.none()
            for item in w:
                a = Auction.objects.filter(id=item.auction_id.id)
                watchlist = list(chain(watchlist, a))

            return render(request, 'bid.html',
            {
                'auction': auction[0],
                'user': user[0],
                'stats': stats,
                'watchlist':watchlist
            })
    except KeyError:
        return index(request)

    return index(request)

def comment(request, auction_id):
    """
    Comment on an auction.

    Returns
    -------
    Function : bid_page(request, auction_id)
        Return the
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            auction = Auction.objects.filter(id=auction_id)
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    msg = Chat()
                    msg.user_id = user[0]
                    msg.auction_id = auction[0]
                    msg.message = form.cleaned_data['comment']
                    msg.time_sent = timezone.now()
                    msg.save()
                    return bid_page(request, auction_id)

            return index(request)
    except KeyError:
        return index(request)

    return index(request)

def raise_bid(request, auction_id):
    """
    Increases the bid of the selected auction
    and returns to the bidding page.

    Parametes
    ---------
    auction_id : class 'int'

    Returns
    -------
    Function : bid_page(request, auction_id)
        Return the bidding page for the selected auction.
    Function : index(request)
        If the user is not logged in.
    """
    auction = Auction.objects.get(id=auction_id)
    if auction.time_ending < timezone.now():
        return bid_page(request, auction_id)
    elif auction.time_starting > timezone.now():
        return index(request)

    try:
        if request.session['username']:
            user = User.objects.get(username=request.session['username'])
            userDetails = UserDetails.objects.filter(user_id=user.id)
            if userDetails.balance > 0.0:
                latest_bid = Bid.objects.filter(auction_id=auction.id).order_by('-bid_time')
                if not latest_bid:
                    increase_bid(user, auction)
                else:
                    current_winner = User.objects.filter(id=latest_bid[0].user_id.id)
                    if current_winner[0].id != user.id:
                        increase_bid(user, auction)

            return bid_page(request, auction_id)
    except KeyError:
        return index(request)

    return bid_page(request, auction_id)

def register_page(request):
    """
    Returns the registration page.

    Returns
    -------
    HTTPResponse
        The registration page.
    """
    return render(request, 'register.html')

def watchlist(request, auction_id):
    """
    Adds the auction to the user's watchlist.

    Returns
    -------
    Function : index(request)
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            auction = Auction.objects.filter(id=auction_id)

            w = Watchlist.objects.filter(auction_id=auction_id)
            if not w:
                watchlist_item = Watchlist()
                watchlist_item.auction_id = auction[0]
                watchlist_item.user_id = user[0]
                watchlist_item.save()
            else:
                w.delete()

            return index(request)
    except KeyError:
        return index(request)

    return index(request)

def watchlist_page(request):
    """
    Disguises the index page to look
    like a page with the auctions the
    user is watching.

    Returns
    -------
    HTTPResponse
        The index page with auctions the user is watching.
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            w = Watchlist.objects.filter(user_id=user[0])

            auctions = Auction.objects.none()
            for item in w:
                a = Auction.objects.filter(id=item.auction_id.id, time_ending__gte=timezone.now())
                auctions = list(chain(auctions, a))
            return render(request, 'index.html', {
                'auctions': auctions,
                'user': user[0],
                'watchlist':auctions
            })
    except KeyError:
        return index(request)

def balance(request):
    """
    If the user is logged in returns
    a HTTPResponse with the page that
    allows the user to update his or her balance.

    Returns
    -------
    HTTPResponse
        The page with the user information
        that updates the account's balance.
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            return render(request, 'balance.html', {'user': user[0]})
    except KeyError:
        return index(request)

    return index(request)

def topup(request):
    """
    Adds credit to user's current balance.

    Returns
    -------
    Function : index(request)
        If the user is not logged in.
    """
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            try:
                if request.session['username']:
                    user = User.objects.get(username=request.session['username'])
                    userDetails = UserDetails.objects.get(user_id=user.id)
                    userDetails.balance += form.cleaned_data['amount']
                    userDetails.save()
            except KeyError:
                return index(request)

    return index(request)

def filter_auctions(request, category):
    """
    Searches current and future auctions
    that belong in a category.

    Parameters
    ----------
    category : class 'str'
        The category name.

    Returns
    -------
    Function : index(request)
         If the user is not logged in.
    """
    f_auctions = []
    if category == "laptops":
        f_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="LAP"
            ).order_by('time_starting')

    elif category == "consoles":
        f_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="CON"
            ).order_by('time_starting')

    elif category == "games":
        f_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="GAM"
            ).order_by('time_starting')

    elif category == "gadgets":
        f_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="GAD"
            ).order_by('time_starting')

    elif category == "tvs":
        f_auctions = Auction.objects.filter(
            time_ending__gte=datetime.now(), product_id__category="TEL"
            ).order_by('time_starting')

    try:
        if request.session['username']:
            auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')
            user = User.objects.filter(username=request.session['username'])

            w = Watchlist.objects.filter(user_id=user[0])
            watchlist = Auction.objects.none()
            for item in w:
                a = Auction.objects.filter(id=item.auction_id.id)
                watchlist = list(chain(watchlist, a))
            print(1)
            return render(request, 'index.html', {'auctions': f_auctions, 'user': user[0], 'watchlist': watchlist})
    except:
        return render(request, 'index.html', {'auctions': tel_auctions})

    return index(request)

def register(request):
    """
    Registration POST request.

    Returns
    -------
    Function
        Index page request
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            is_valid = validate_registration(
                form.cleaned_data['username'],
                form.cleaned_data['password1'],
                form.cleaned_data['password2'],
                form.cleaned_data['email']
            )
            if is_valid:
                # Create an User object with the form parameters.
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password1'])
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.save()  # Save the object to the database.
                userDetails = UserDetails()
                userDetails.balance = 0.0
                userDetails.cellphone = form.cleaned_data['cellphone']
                userDetails.address = form.cleaned_data['address']
                userDetails.town = form.cleaned_data['town']
                userDetails.post_code = form.cleaned_data['postcode']
                userDetails.country = form.cleaned_data['country']
                userDetails.user_id = user
                userDetails.save()
    return index(request)

def login_page(request):
    """
    Login POST request.
        
    Returns
    -------
    Function
        Index page request    
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            is_valid = validate_login(
                form.cleaned_data['username'], 
                form.cleaned_data['password']
            )
            if is_valid :
                # Creates a session with 'form.username' as key.
                request.session['username'] = form.cleaned_data['username']
    return index(request)

def logout_page(request):
    """
    Deletes the session.
    
    Returns
    -------
    Function
        Index page request
    """
    try:
        del request.session['username']
    except:
        pass # if there is no session pass
    return index(request)