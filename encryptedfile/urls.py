from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    path('', views.FileListView.as_view(), name='file_list'),
    path('new', views.file_uplod_to_server, name='add_file'),
    path('download/<int:pk>', views.download_encrypted_file, name='download_file'),
    path('detail/<int:pk>', views.FileDetailView.as_view(), name='file_detail'),
    path('update/<int:pk>', views.FileUpdateView.as_view(), name='file_update'),
    path('delete/<int:pk>', views.FileDeleteView.as_view(), name='file_delete'),
    path('forgot/<int:pk>', views.forgot_key, name='file_forgot_key'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]