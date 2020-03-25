from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.urls import reverse
from XHacker.models import user_post

from registrationapp.models import UserProfileModel, Friend
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.template.context_processors import csrf
from django.views.generic import UpdateView
from .forms import ProfileForm, userProfile
from XHacker.forms import *
from XHacker.models import serviec
from .forms import *
from XHacker.forms import userEditPost
from XHacker.models import comments
from XHacker.views import contactUsSucess


@login_required(login_url='/signin')
def special(request):
    return render(request, 'register/sp.html')


def logout_view(request, ):
    logout(request)


@login_required(login_url="/signin")
def create_service(request):
    form = modelForm(request.POST, request.FILES)
    if request.method == 'POST':
        savedata = form.save(commit=False)
        savedata.name = form.cleaned_data['name']
        savedata.description = form.cleaned_data['description']
        savedata.image = form.cleaned_data['image']
        savedata.user = request.user
        savedata.save()
        html = "<Html><body>Congratulation!! Your post has been uploaded sucessful,<a href='/allpost'><button style='color:red;'>Refresh</button></a></body></html>"

        return HttpResponse(html)
    else:
        form = modelForm()
    return render(request, 'lala/add_new_thought.html', {
        'form': form
    })


def detail(request, slug):
    q = serviec.objects.filter(slug=slug)
    allpost=serviec.objects.all()

    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Post Not Found</h1>')
    context = {

        'post': q,
        'allpost':allpost,

    }
    return render(request, 'get.html', context)


def forum(request):
    user = User.objects.all()

    post = serviec.objects.all().order_by('-created_date')
    query = request.GET.get('q')
    if query:
        post = serviec.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username=query)

        )

    return render(request, 'AllForumPost.html', {'post': post, 'user': user})


def edit_post(request, slug):
    instance = get_object_or_404(serviec, slug=slug)
    form = editModelForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('allpost')
    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, 'XHacker/serviec_form.html', context)


def delete(request, slug=None):
    instance = get_object_or_404(serviec, slug=slug)
    if request.method == 'POST':
        instance.delete()
        return redirect(forum)
    context = {'post': instance}
    return render(request, 'delete_post.html', context)




def user_profile(request):
    profile = ProfileForm(request.POST, request.FILES)
    if request.method == "POST":
        p = profile.save(commit=False)
        p.bio = profile.cleaned_data['bio']
        p.website = profile.cleaned_data['website']
        p.user_image = profile.cleaned_data['user_image']
        p.user = request.user
        p.save()
        return redirect('/')
    else:
        profile = ProfileForm()
    return render(request, 'profile.html', {
        'profile': profile
    })


def profile(request, username):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofilemodel)
        if form.is_valid() and (username == request.user.username):
            form.save()
            messages.success(request, 'Profile Updated Sucessfully..!!!')
            return redirect("/profile/" + str(request.user.username))
        else:
            return redirect(sucess_edit)
    else:
        form = ProfileForm(instance=request.user.userprofilemodel)
    return render(request, 'edit_profile.html', {'form': form})


@login_required(login_url='/signin')
def about(request, username=None, id=None):
    user = User.objects.get(username=username)

    p = UserProfileModel.objects.get(user=user)
    q = user_post.objects.filter(author=user).order_by('-created_date')
    com = comments.objects.all().filter(id=id)

    post = post_upload_form(request.POST or None, request.FILES)
    if request.method == 'POST':
        p = post.save(commit=False)
        p.title = post.cleaned_data['title']
        p.text = post.cleaned_data['text']
        p.image = post.cleaned_data['image']
        p.author = request.user
        p.save()

        return redirect("/profile/" + str(request.user.username))
    else:
        post = post_upload_form()

    context = {
        'profile_user': user,
        'p': p,
        'u_post': q,
        'post': post,
        'com': com

    }

    #  if request.is_ajax():
    #     html=render_to_string('about.html',context,request=request)
    #
    #       return JsonResponse({'forms':html})
    #

    return render(request, 'about.html', context)


def sucess_edit(request):
    return render(request, 'Edit_sucessful.html')


def pic_change(request, username):
    if request.method == "POST":
        form = profile_pic(request.POST, request.FILES, instance=request.user.userprofilemodel)
        if form.is_valid() and (username == request.user.username):
            form.save()
            messages.success(request, 'Your profile has been updated sucessfully.!!')
            return redirect("/profile/" + str(request.user.username))
        else:
            return redirect(sucess_edit)
    else:
        form = ProfileForm(instance=request.user.userprofilemodel)
    return render(request, 'edit_profile_pic.html', {'form': form})


def upload_user_post(request):
    post = post_upload_form(request.POST or None, request.FILES)
    if request.method == 'POST':
        p = post.save(commit=False)
        p.title = post.cleaned_data['title']
        p.text = post.cleaned_data['text']
        p.image = post.cleaned_data['image']
        p.author = request.user

        p.save()
        messages.success(request, 'Your post has been sucessfully uploaded..!!')

        return redirect("profile/" + str(request.user.username))
    else:
        post = post_upload_form()
    context = {'post': post}
    return render(request, 'uplod_user_post.html', context)


def user_post_edit(request, slug=None):
    instance = get_object_or_404(user_post, slug=slug)
    form = userEditPost(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid() and instance.author == request.user:
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, 'Your post has been sucessfully updated..!!')
        return HttpResponseRedirect("/newsfeed")

    return render(request, 'edit_user_post.html', {'post': form})


def delete_user_post(request, slug=None):
    instance = get_object_or_404(user_post, slug=slug)
    if request.method == 'POST':
        instance.delete()
        messages.success(request,"Your post has been deleted sucessfully..!!")
        return HttpResponseRedirect("/newsfeed")
    context = {'post': instance}
    return render(request, 'delete_user_post_confirm.html', context)


def like_post(request):
    post = get_object_or_404(user_post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect(special)


def ap(request, id=None):
    apa = user_post.objects.filter(author=request.user)
    postL = user_post.objects.get(id=id)
    p = comments.objects.all().filter(post=id)
    return render(request, 'ap.html', {'ap': apa, 'obj': p, 'obla': postL})


def show(request, id=None):
    q = user_post.objects.get(id=id)

    p = comments.objects.all().filter(post=id).order_by('-commented_date')
    posts = get_object_or_404(user_post, id=id)
    pst = serviec.objects.all().order_by('-created_date')
    query = request.GET.get('q')
    if query:
        pst = serviec.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username=query)

        )

    if request.method == "POST":
        forms = CommentForm(request.POST or None)

        if forms.is_valid():
            comment_form = request.POST.get('comment')
            c1 = comments.objects.create(post=posts, user=request.user, comment=comment_form)
            c1.save()

        # return redirect(special)
    else:
        forms = CommentForm()
    context = {'datum': q, 'comments': p, 'form_form': forms, 'post': posts, 'pst': pst}

    if request.is_ajax():
        html = render_to_string('show.html', context, request=request)

        return JsonResponse({'forms': html})
    return render(request, 'show.html', context)


def upload_sucess(request):
    return render(request, 'pkk.html')

@user_passes_test(lambda u: u.is_superuser)
def adminMessage(request):
    p=ContactUsModel.objects.all()
    return render(request, 'allmessageAdmin.html', {'messages': p})

def contactUsForm(request):
    cForm = ContactUsForm(request.POST or None)
    if request.method == 'POST':
        f = cForm.save(commit=False)
        f.name = cForm.cleaned_data['name']
        f.email = cForm.cleaned_data['email']
        f.message = cForm.cleaned_data['message']
        f.save()
        return redirect(contactUsSucess)
    else:
        cForm = ContactUsForm()
    context = {'cForm': cForm, }
    return render(request,'contactUsForm.html',context)

def profile_user(request):
    return redirect("/profile/" + str(request.user.username))


def add_or_remove_friends(request, username, verb):
    n_f = get_object_or_404(User, username=username)
    owner = request.user
    new_friend = UserProfileModel.objects.get(user=n_f)

    if verb == "add":
        new_friend.followers.add(owner)
        Friend.make_friend(owner, new_friend)
    else:
        new_friend.followers.remove(owner)
        Friend.remove_friend(owner, new_friend)

    return redirect(new_friend.get_absolute_url())

def list_friends(request):
    friend_object, created = Friend.objects.get_or_create(current_user=request.user.userprofilemodel)
    friends = [friend for friend in friend_object.users.all()]
    return render(request, 'template.html', {"friends":friends})


def newsfeed(request,id=None):

    post=user_post.objects.all().order_by('-created_date')
    user = User.objects.all()

    post_upload = post_upload_form(request.POST or None, request.FILES)
    if request.method == 'POST':
        p = post_upload.save(commit=False)
        p.title = post_upload.cleaned_data['title']
        p.text = post_upload.cleaned_data['text']
        p.image = post_upload.cleaned_data['image']
        p.author = request.user
        p.save()
        messages.success(request,'Your post has been Added')
        return HttpResponseRedirect("/newsfeed")
    else:
        post_upload=post_upload_form()

    context={'post':post,'user':user,'post_upload':post_upload_form,}
    return render(request,'newsfeed.html',context)