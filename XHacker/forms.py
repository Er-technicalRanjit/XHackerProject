from django.forms import ModelForm
from django import forms

from .models import serviec, user_post, comments, Software_Review


class modelForm(ModelForm):
    class Meta:
        model = serviec
        fields = ['name', 'description', 'image']


class editModelForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-danger', 'placeholder': 'title'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control bg-danger', 'placeholder': 'Post description..'}))

    class Meta:
        model = serviec
        fields = ['name', 'description', 'image']


class post_upload_form(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter your username'}),
        max_length=50)
    text = forms.Textarea()
    image = forms.ImageField(required=False)

    class Meta:
        model = user_post
        fields = ['title', 'text', 'image']


class userEditPost(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-danger', 'placeholder': 'title'}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control bg-danger', 'placeholder': 'Drop your Comments here...!!!'}))

    class Meta:
        model = user_post
        widgets = {'image': forms.FileInput(
            attrs={'class': 'form-control'}
        )}
        fields = ['title', 'text', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['comment']


class SoftwareReviewForm(forms.ModelForm):
    class Meta:
        model = Software_Review
        fields = ['review']
