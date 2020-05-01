from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
# Create your views here.
from customuser.models import MyUser
from userprofile.models import UserProfile
from .models import EncryptedFile
from .forms import EncryptedFileForm, CreateFileForm
import os
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

buffer_size = 65536  # 64kb
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


access_token_generator = TokenGenerator()


class FileListView(LoginRequiredMixin, ListView):
    """ list view of encrypted files """
    model = EncryptedFile
    template_name = "encryptedfile/file_list.html"


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        print(self.request.user.id)
        log_entries = []
        logs = LogEntry.objects.all()
        for i in logs:
            if i.__str__().__contains__(self.request.user.email):
                print("inside this",self.request.user.email)
                log_entries.append(i.__str__())
        profile = get_object_or_404(UserProfile, owner=self.request.user)
        context['log_entries']=log_entries
        context['profile'] = profile
        return context


def handle_upload_file(request, file, fileName):
    destination = os.path.join(settings.MEDIA_ROOT, "user_" + request.user.username, "file")
    if not os.path.exists(destination):
        os.makedirs(destination)

    file_path = destination + "\\" + fileName + os.path.splitext(file.name)[1]
    output_file = open(file_path + '.encrypted', 'wb+')

    key = get_random_bytes(32)  # Use a stored / generated key
    cipher_encrypt = AES.new(key, AES.MODE_CFB)
    output_file.write(cipher_encrypt.iv)

    buffer = file.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher_encrypt.encrypt(buffer)
        output_file.write(ciphered_bytes)
        buffer = file.read(buffer_size)
    file.close()
    output_file.close()

    return output_file.name, key


@login_required()
def file_uplod_to_server(request):
    """ test upload file and encrypt it"""
    form = CreateFileForm(None)

    if request.method == 'POST':
        form = CreateFileForm(request.POST, request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            fileInput = request.FILES['file_url']
            fileName = form.cleaned_data.get('file_name')
            file, key = handle_upload_file(request, fileInput, fileName)
            form_save.file_url = file
            form_save.file_key = key
            form_save.user = request.user
            form_save.save()
            return redirect('file_list')

    return render(request, 'encryptedfile/add_file.html', {
        'form': form
    })


def decripty_file(request, encypted_file):
    input_file = open(encypted_file.file_url.path, 'rb')
    output_file = open(encypted_file.file_url.path[:-10], 'wb')
    iv = input_file.read(16)

    cipher_encrypt = AES.new(encypted_file.file_key, AES.MODE_CFB, iv=iv)

    # Keep reading the file into the buffer, decrypting then writing to the new file
    buffer = input_file.read(buffer_size)
    while len(buffer) > 0:
        decrypted_bytes = cipher_encrypt.decrypt(buffer)
        output_file.write(decrypted_bytes)
        buffer = input_file.read(buffer_size)

    # Close the input and output files
    input_file.close()
    output_file.close()
    return output_file.name


def sendMailToUser(request, name):
    mail_subject = "Downloading file {} ".format(name)
    current_site = get_current_site(request)
    # message = render_to_string('encryptedfile/acc_active_email.html', {
    #     'user': request.user,
    #     'domain': current_site.domain,
    #     'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
    #     'token': access_token_generator.make_token(request.user),
    # })
    #
    message = request.user.username + " try to get file " + name
    to_email = request.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


def activate(request, uidb64, token):
    user = request.user
    uid = force_text(urlsafe_base64_decode(uidb64))
    # user = MyUser.objects.get(pk=uid)


    # except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
    #     user = None
    # if user is not None and access_token_generator.check_token(user, token):
    #     user.is_active = True
    #     user.save()
    #     # return redirect('home')
    #     return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    # else:
    return redirect(reverse('file_update', args=uid))


@csrf_exempt
def download_encrypted_file(request, pk):
    """ reply to ajax request to download """
    encypted_file = get_object_or_404(EncryptedFile, pk=pk)

    # sendMailToUser(request, encypted_file.file_name)

    isAutheticated = False

    password = request.POST.get('data')
    output_file = "",
    print(password, encypted_file.file_password)
    if password == encypted_file.file_password:
        isAutheticated = True
        output_file = decripty_file(request, encypted_file)

    data = {
        "isAutheticated": isAutheticated,
        "file": output_file,
        "fileName": encypted_file.file_name,

    }

    return JsonResponse(data, safe=False)


class AddEncryptedField(LoginRequiredMixin, CreateView):
    """ create view for uploading files """
    template_name = 'encryptedfile/add_file.html'
    form_class = EncryptedFileForm
    success_url = reverse_lazy('file_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class FileDetailView(LoginRequiredMixin, DetailView):
    """ detail view for file """
    model = EncryptedFile
    template_name = "encryptedfile/file_detail.html"


class FileUpdateView(LoginRequiredMixin, UpdateView):
    """ update view for encrypted file"""
    model = EncryptedFile
    form_class = EncryptedFileForm
    template_name = 'encryptedfile/add_file.html'


class FileDeleteView(LoginRequiredMixin, DeleteView):
    """ delete view for file"""
    model = EncryptedFile
    template_name = "encryptedfile/file_delete.html"
    success_url = "/files"


def setMailToForgot(request, pk):
    mail_subject = "Forgot Key "
    current_site = get_current_site(request)
    message = render_to_string('encryptedfile/acc_active_email.html', {
        'user': request.user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(pk)),
        'token': access_token_generator.make_token(request.user),
    })

    # message = request.user.username + " try to get file " + name
    to_email = "mbjithinbabu@gmail.com"
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


@login_required()
def forgot_key(request, pk):
    setMailToForgot(request, pk)
    return HttpResponse("check your mail")
