from django.urls import  path

from . import views


urlpatterns = [
    path('', views.feedback_home, name='feedback_home'),
    path('create', views.add_feed_back, name='add_feedback'),
]