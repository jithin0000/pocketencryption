from django import forms

from userprofile.models import UserProfile


class UserProfileForm(forms.ModelForm):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'type' :'number'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'type' :'number'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'type' :'date'}))
    class Meta:
        model = UserProfile
        exclude =['owner',]