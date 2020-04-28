from django.shortcuts import render

# Create your views here.

def home(request):
    """ home view function """

    return render(request, 'home/home.html', {})
