from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages

# Create your views here.
from .forms import RegisterForm, LoginForm

def register_user(request):
    """ view for register """
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('login')
    
    return render(request, 'customuser/register.html', { 'form': form})


def login_user(request):
    """ login view """

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('adhar_id'), password=form.cleaned_data.get('password'))
            if user is not None:
                user = login(request, user)
                return redirect('file_list')
            else:
                messages.error(request, "username or password is invalid")

    
    return render(request, 'customuser/login.html', { 
        'form' : form  })
