from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from registrationapp.views import *

from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponseRedirect
from django.urls import reverse

# from formapp import templates
# from formapp.models import *

from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from datetime import timezone
from django.utils import timezone
from registrationapp.forms import form
from .models import SoftwareModel


def index(request):
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

    return render(request, "index.html", context)


def contactUsSucess(request):
    return render(request, 'contactUsSucess.html')


def formview(request):
    if request.method == 'POST':
        form1 = form(request.POST)

        if form1.is_valid():
            form1.save()
            return render(request, 'signup.html', {'form': form1})
    else:
        form1 = form()
    return render(request, 'signup.html', {'form': form1})


def logout_confirm(request):
    return render(request, 'logout_confirm.html')


def register(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are logged in please logout first')
        return redirect("profile/" + str(request.user.username))
    else:
        if request.method == 'POST':
            forms = form(request.POST)
            if forms.is_valid():
                username = forms.cleaned_data['username']
                email = forms.cleaned_data['email']
                first_name = forms.cleaned_data['first_name']
                last_name = forms.cleaned_data['last_name']
                password = forms.cleaned_data['password']
                User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                         password=password)

                return HttpResponseRedirect('/signin')

        else:

            forms = form()

        return render(request, 'signup.html', {'form': forms})


def login(request):
    if request.user.is_authenticated:
        return redirect("profile/" + str(request.user.username))

    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)

                    return redirect("profile/" + str(request.user.username))
                elif username == "":

                    messages.error(request, 'Please Enter your username')
                elif password == "":
                    messages.error(request, 'Please Enter your password')


                else:
                    messages.error(request, 'Username and password doesnot match')


            except User.DoesNotExist:
                pass

        return render(request, 'registration/login.html')


from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)

    return HttpResponseRedirect('/signin')


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def AboutUs(request):
    return render(request, "aboutUs.html")


def TermsAndCondition(request):
    return render(request, "TermsAndCondition.html")


def softwareMainPage(request):
    obj = SoftwareModel.objects.all()

    return render(request, "Software Templates/software_mainPage.html", {'obj': obj})


def Software_details(request,slug,pk):
    post=get_object_or_404(SoftwareModel,pk=pk,slug=slug,)
    allpost = SoftwareModel.objects.all()
    reviews=Software_Review.objects.filter(soft_post=post)

    if request.method=='POST':
        review=SoftwareReviewForm(request.POST or None)
        if review.is_valid():
            rv=request.POST.get('review')
            save=Software_Review.objects.create(soft_post=post,posted_user=request.user,review=rv)
            save.save()
            return HttpResponseRedirect(request.path_info)
    else:
        review=SoftwareReviewForm()






    context={'post':post,'review':review,'allpost':allpost,'reviews':reviews}
    return render(request,'Software Templates/softwareSinglePost.html',context)
