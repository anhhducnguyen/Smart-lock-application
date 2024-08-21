from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GoogleSSOUser(models.Model):
    google_id = models.CharField(max_length=255, unique=True)
    locale = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username