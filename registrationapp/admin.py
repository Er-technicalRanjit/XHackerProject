from django.contrib import admin
from .models import UserProfileModel,ContactUsModel,Friend

admin.site.register(UserProfileModel)
admin.site.register(Friend)

class ContactUsModelAdmin(admin.ModelAdmin):

    list_display = ['name','email','message','sent_date']

admin.site.register(ContactUsModel,ContactUsModelAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
