from django.urls import path


from . import views

urlpatterns = [
    path('', views.FileListView.as_view(), name='file_list'),
    path('new', views.file_uplod_to_server, name='add_file'),
    path('download/<int:pk>', views.download_encrypted_file, name='download_file'),
]