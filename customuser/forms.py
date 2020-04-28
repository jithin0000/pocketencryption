from django import forms

from .models import MyUser

class RegisterForm(forms.ModelForm):
    """ form for register """

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = MyUser
        fields=['email','adhar_id','username','password']


class LoginForm(forms.Form):
    """ form for login form """
    adhar_id = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())