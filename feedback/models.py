from django.db import models

# Create your models here.
from customuser.models import MyUser

class FeedBack(models.Model):
    """ user feedback model """
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    feedback = models.TextField()

    def __str__(self):
        return self.title
