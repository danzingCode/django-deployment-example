from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# we dint want to inherit directly from User, that's why we use UserProfileInfo(models.Model)
class UserProfileInfo(models.Model):
    # We create this class to get some additional information to the User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
