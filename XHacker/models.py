from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from registrationapp.models import UserProfileModel

from XHackerProject.utils import unique_slug_generator, unique_slug_generators


class About(models.Model):
    short_description = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="about")

    class Meta:
        verbose_name = "About me"
        verbose_name_plural = "About me"

        def __str__(self):
            return "About me"


class serviec(models.Model):
    slug = models.SlugField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Service name")
    description = models.TextField(verbose_name="About service", blank=True)
    image = models.ImageField(upload_to="image", blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


def rl_pre_save_receivers(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generators(instance)


pre_save.connect(rl_pre_save_receivers, sender=serviec)


class RecentWork(models.Model):
    title = models.CharField(max_length=100, verbose_name="Work Name")
    image = models.ImageField(upload_to="Works")

    def __str__(self):
        return self.title


class client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Client Name")
    description = models.TextField(verbose_name="Client Details")
    image = models.ImageField(upload_to="Client")

    def __str__(self):
        return self.name


class user_post(models.Model):
    slug = models.SlugField(max_length=250, null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to="post_image", blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    def published(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/profile/{self.author.username}'

    def total_likes(self):
        return self.likes.count()


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=user_post)


class comments(models.Model):
    post = models.ForeignKey(user_post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    commented_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))


class SoftwareModel(models.Model):
    slug = models.SlugField(max_length=250, null=True, blank=True)
    software_name = models.CharField(max_length=255)
    soft_desc1 = models.TextField(max_length=1500, blank=True)
    soft_desc2 = models.TextField(max_length=2000, blank=True)
    image1 = models.ImageField(upload_to="softwareImage", blank=True)
    image2 = models.ImageField(upload_to="softwareImage", blank=True)
    download_link = models.CharField(max_length=300, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.software_name


def rl_pre_save_receiverss(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generators(instance)


pre_save.connect(rl_pre_save_receiverss, sender=SoftwareModel)


class Software_Review(models.Model):
    soft_post=models.ForeignKey(SoftwareModel,on_delete=models.CASCADE)
    posted_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=300)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.soft_post.software_name, str(self.posted_user.username),str(self.review))
