from django import forms
from .models import CityZen

class CityZenForm(forms.ModelForm):
    """ form for creating and updating cityzen """

    class Meta:
        model = CityZen
        fields="__all__"