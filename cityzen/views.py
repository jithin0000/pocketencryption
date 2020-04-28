from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView
# Create your views here.
from .forms import CityZenForm

class CityZenCreateView(LoginRequiredMixin,CreateView):
    """ add cityzen class based view """
    form_class = CityZenForm
    template_name="cityzen/add_cityzen.html"
    success_url=reverse_lazy('add_cityzen')

