from django.db import models

# Create your models here.
from django.urls import reverse

from customuser.models import MyUser

def user_file_upload(instance, filename):
    return "user_{0}/file/{1}".format(instance.user.username, filename)

class EncryptedFile(models.Model):
    """ encrypted file model """
    user= models.ForeignKey(MyUser, on_delete=models.CASCADE)
    file_name=models.CharField(max_length=100)
    file_password = models.CharField(max_length=255)
    file_key = models.BinaryField(editable=False,max_length=255)
    file_url = models.FileField(upload_to=user_file_upload)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('file_detail',kwargs={ 'pk', self.id})

    def __str__(self):
        return self.file_name
