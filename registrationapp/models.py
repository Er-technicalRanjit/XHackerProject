import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from django_countries.fields import CountryField
from django_countries import countries




class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    choices = ("Male", "Male"), ("Female", "Female"), ("Others", "Others")
    gender = models.CharField(max_length=9, choices=choices, default="Male")
    country = CountryField(choices=list(countries))

    user_image = models.ImageField(upload_to="profie", blank=True, default="default.jpg")

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfileModel.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


# Create your models here.
class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=1000)
    sent_date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.name


class Friend(models.Model):
    users = models.ManyToManyField(UserProfileModel)
    current_user = models.ForeignKey(UserProfileModel, related_name="owner", null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

    def __str__(self):
        return str(self.current_user)
