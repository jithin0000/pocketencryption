from django import forms

from .models import EncryptedFile

class EncryptedFileForm(forms.ModelForm):
    """ form for encrypted file """
    file_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = EncryptedFile
        fields=['file_password',]


class CreateFileForm(forms.ModelForm):
    """ form for encrypted file """
    file_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = EncryptedFile
        fields=['file_name','file_password','file_url']