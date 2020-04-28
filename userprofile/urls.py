from django.urls import path

from . import views

urlpatterns = [
        path('', views.user_profile_detail_view, name='profile_detail'),
        path('update/<int:pk>', views.ProfileUpdateView.as_view(), name='profile_update'),
        ]
