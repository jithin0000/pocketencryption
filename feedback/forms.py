from django import forms

from feedback.models import FeedBack


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['title','feedback']