from django.contrib import admin
from .models import *

admin.site.register(comments)
admin.site.register(Software_Review)


class ServiecAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(serviec, ServiecAdmin)


# Register your models here.
class UserpostAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(user_post, UserpostAdmin)

admin.site.register(SoftwareModel)
