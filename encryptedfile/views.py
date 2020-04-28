from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
# Create your views here.
from .models import EncryptedFile
from .forms import EncryptedFileForm
import os
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class FileListView(LoginRequiredMixin,ListView):
    """ list view of encrypted files """
    model = EncryptedFile
    template_name="encryptedfile/file_list.html"
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(user = self.request.user)
        return queryset


def handle_upload_file(request,file):

    destination = os.path.join(settings.MEDIA_ROOT,"user_"+ request.user.username,"file")
    if not os.path.exists(destination):
        os.makedirs(destination)

    file_path = destination + "\\" + file.name
    output_file = open(file_path + '.encrypted', 'wb+')

    key = get_random_bytes(32)  # Use a stored / generated key
    buffer_size = 65536  # 64kb
    cipher_encrypt = AES.new(key, AES.MODE_CFB)
    output_file.write(cipher_encrypt.iv)

    buffer = file.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher_encrypt.encrypt(buffer)
        output_file.write(ciphered_bytes)
        buffer = file.read(buffer_size)
    file.close()
    output_file.close()

    return output_file.name,key



def file_uplod_to_server(request):
    """ test upload file and encrypt it"""
    form = EncryptedFileForm(None)

    if request.method == 'POST':
        form = EncryptedFileForm(request.POST, request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            file, key = handle_upload_file(request,request.FILES['file_url'])
            form_save.file_url = file
            form_save.file_key = key
            form_save.user = request.user
            form_save.save()
            return redirect('file_list')

    return render(request, 'encryptedfile/add_file.html',{
        'form' : form
    })


def download_encrypted_file(request, pk):
    """ reply to ajax request to download """
    encypted_file = get_object_or_404(EncryptedFile, pk=pk)
    print()

    data = {
        "file" : encypted_file.file_url.url[:-10]
    }

    return JsonResponse(data, safe=False)


class AddEncryptedField(LoginRequiredMixin,CreateView):
    """ create view for uploading files """
    template_name='encryptedfile/add_file.html'
    form_class = EncryptedFileForm
    success_url=reverse_lazy('file_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())