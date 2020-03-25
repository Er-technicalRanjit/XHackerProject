from django.forms import ModelForm
from django.shortcuts import render
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.validators import validate_email

from XHacker.forms import modelForm
from .models import UserProfileModel,ContactUsModel


class form(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter your username'}),
        max_length=50)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter your Email'}),
        max_length=50)
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter your First Name'}),
        max_length=50)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter your Last Name'}),
        max_length=50)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter your Password'}),
        max_length=50)

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control rounded-pill', 'placeholder': 'Confirm your password'}), max_length=50)

    class Meta():
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

    def clean_email(self):
        email1 = self.cleaned_data['email']
        try:
            match = User.objects.get(email=email1)

        except:
            return self.cleaned_data['email']
        raise forms.ValidationError("User already exists with this email")

    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            match = User.objects.get(username=user)

        except:
            return self.cleaned_data['username']
        raise forms.ValidationError("User already exists with this username")

    def clean_confirm_password(self):
        pas = self.cleaned_data['password']
        con_pas = self.cleaned_data['confirm_password']
        min_password = 8
        if pas and con_pas:
            if pas != con_pas:
                raise forms.ValidationError("Password doesnot match")
            else:
                if len(pas) < min_password:
                    raise forms.ValidationError("Your password must be 8 character long")
                if pas.isdigit():
                    raise forms.ValidationError("Password Should not contain digit only")


class userProfile(ModelForm):
    class Meta():
        model = User
        fields = ['email']


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-danger', 'placeholder': 'bio'}))
    website = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-danger', 'placeholder': 'website'}))

    class Meta():
        model = UserProfileModel
        fields = ['bio', 'website', 'user_image','gender','country']


class profile_pic(forms.ModelForm):
    class Meta():
        model = UserProfileModel
        fields = ['user_image']


class ContactUsForm(forms.ModelForm):
    class Meta:
        model=ContactUsModel
        fields=['name','email','message']