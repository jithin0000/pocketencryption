from django import forms

from .models import EncryptedFile

class EncryptedFileForm(forms.ModelForm):
    """ form for encrypted file """

    class Meta:
        model = EncryptedFile
        exclude=['user']