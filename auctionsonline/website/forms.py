from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=45)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=45)
    password2 = forms.CharField(max_length=45)
    firstname = forms.CharField(max_length=56)
    lastname = forms.CharField(max_length=45)
    cellphone = forms.CharField(max_length=45)
    address = forms.CharField(max_length=255)
    town = forms.CharField(max_length=45)
    postcode = forms.CharField(max_length=45)
    country = forms.CharField(max_length=45)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=45)
    password = forms.CharField(max_length=45)

