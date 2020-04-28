from django.urls import path

from .views import register_user, login_user, logout_view

urlpatterns = [
    path('register', register_user, name="register"),
    path('login', login_user, name="login"),
    path('logout', logout_view, name="logout"),

]