from django.urls import path

from .views import CityZenCreateView

urlpatterns = [
    path('', CityZenCreateView.as_view(), name="add_citizen",)

]