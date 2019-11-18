# on your terminal
#   $ python manage.py runscript do_migrations --script-args copyDataFromUserDetails
#   or
#   $  python manage.py runscript do_migrations --script-args setUserIDs
#
#   (!) install django-extensions
#   (!) Don't forget to add 'django_extensions' in your settings.py

from django.contrib.auth.models import User
from website.models import UserDetails


def copy_data_from_user_details():
    """ Execute after renaming model 'User' to 'UserDetails'
        Copies password, email, first and last name UserDetails to the matching auth_user record.
    """
    user_details = UserDetails.objects.all()
    for ud in user_details:
        auth_user = User.objects.filter(id = ud.id)
        if(not auth_user):  # auth_user record doesn't exist | create one
            new_user = User.objects.create_user(ud.username, ud.email, ud.password)
            new_user.last_name = ud.lastname
            new_user.first_name = ud.firstname
            new_user.save()
        else: # update details
            if auth_user.get().username != ud.username:
                ud.delete()
            ex_auth_user = auth_user.get()
            ex_auth_user.set_password(ud.password)
            ex_auth_user.email = ud.email
            ex_auth_user.first_name = ud.firstname
            ex_auth_user.last_name = ud.lastname
            ex_auth_user.save()


def set_user_ids():
    """ Populates new UserDetail's field user_id with the auth_user id.
    """
    user_details = UserDetails.objects.all()
    for ud in user_details:
        auth_user = User.objects.filter(id=ud.id)
        if auth_user:  # auth_user record doesn't exist | create one
            ud.user_id = auth_user.get().id
            ud.save()


def run(*args):
    if len(args) != 1:
        print('Invalid use of this script')
        print("Call script with argument 'copyDataFromUserDetails' or 'setUserIDs'")
    elif args[0] == 'copyDataFromUserDetails':
        copy_data_from_user_details()
    elif args[0] == 'setUserIDs':
        set_user_ids()
