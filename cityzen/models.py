from django.db import models

# Create your models here.
from customuser.models import MyUser

def user_directory_path(instance, filename):
    """ giver image field a path """
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class CityZen(models.Model):
    """ model for city zen """
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    mobile = models.IntegerField(default=0)
    date_of_birth=models.DateTimeField()
    state=models.CharField(max_length=255)
    city=models.CharField(max_length=100)
    image_url = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.user.username
