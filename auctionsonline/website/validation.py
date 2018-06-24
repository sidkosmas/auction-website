# login validation func (pass validation email validation), register validation,
from website.models import User
from website.forms import *

def validate_login(username, password):
    user = User.objects.filter(username=username)
    if not user:
        return False
    passw = User.objects.filter(username=user[0].username, password=password)
    if passw[0].password == password :
        return True
    return False

def validate_registration(username, password1, password2, email):
    user = User.objects.filter(username=username)
    if not user:
        check = User.objects.filter(username=user[0].username, email=email)
        if password1 is not password2 :
            print("password confirm not compatible")
            return False, problem
        if check[0].email == email :
            print("email already exists")
            return False
    else:
        print("user already exists")
        return False
    return False