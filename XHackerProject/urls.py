"""HackerProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin


from django.urls import path,include

from XHackerProject import settings
from registrationapp import views as v
from XHacker.views import *


urlpatterns = [
    path('friend/',v.list_friends,name="friends"),
    path('newsfeed',v.newsfeed,name="newsfeed"),
    path('privacy_policy/',privacy_policy,name='privacy_policy'),
    path('aboutUs/',AboutUs,name='AboutUs'),
    path('TermsAndCondition/',TermsAndCondition,name='TermsAndCondition'),
    path('admin/', admin.site.urls),
    path('wrong',v.sucess_edit,name="wronguser"),
    path('ap/',v.ap,name='ap'),
    path('allmessage/',v.adminMessage,name="allmessage"),
    path('contactUsSucess/',contactUsSucess,name="ContactUsSucess"),
    path('contactUs',v.contactUsForm,name="contactUs"),
    path('u_profile',v.profile_user,name="u_profile"),
    path('uploaded/',v.upload_sucess,name="uploaded"),
    path('show/<int:id>',v.show,name='show'),
    path('usereditpost/<slug:slug>/edit',v.user_post_edit,name="user_post_edit"),
    path('userpost/<slug>/delete',v.delete_user_post,name="delete_user_post"),
    path('profile/<username>',v.about,name="user_profile"),
    path('profile/<username>/editpic',v.pic_change,name="pic_change"),
    path('profile/<username>/edit',v.profile,name="edit_profile"),
    #path('registers/',v.registers,name="registers"),
    #path('/',include("django.contrib.auth.urls")),
    path('special/',v.special,name="special"),
    #path('logout/',logout_view,name="logout"),
    path('signup',register,name="signup"),
    path('signin', login, name='signin'),
    path('logout/', logout,name="logout"),
    path('allpost/',v.forum,name="allpost"),
    path('useruploadpost/',v.upload_user_post,name="user_upload_post"),
    path('forum/<slug:slug>',v.detail,name="getpost"),
    path('create_service',v.create_service,name="create_service"),
    path('forum/<slug:slug>/edit',v.edit_post,name="update_post"),

    path('forum/<slug>/delete',v.delete,name="delete_post"),
    path('',index,name="home-page"),
    path('like/',v.like_post,name="like_post"),
    path('software/',softwareMainPage,name='softwareMainPage'),
    path('software/<int:pk>/<slug:slug>', Software_details, name="softwareDetails"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

