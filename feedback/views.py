from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from feedback.forms import FeedBackForm
from feedback.models import FeedBack


@login_required()
def add_feed_back(request):
    form = FeedBackForm()

    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_home')

    return render(request, 'feedback/feedback_ad.html', { 'form' : form})


@login_required()
def feedback_home(request):
    feedback = FeedBack.objects.filter(user =request.user)
    return render(request, 'feedback/feedback_list.html',{
        'feedback_list' : feedback
    })
