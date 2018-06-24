# login validation func (pass validation email validation), register validation,
from website.models import User

def validate_login(username, password):
    user = User.objects.filter(username=username)
    if not user:
        return False
    passw = User.objects.filter(username=user[0].username, password=password)
    if passw[0].password == password :
        return True
    return False