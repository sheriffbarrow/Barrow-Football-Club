from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, UserAuthenticationForm, UserUpdateForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from bfc.models import Post
from .import forms
from account.models import Registration
from django.contrib.auth.decorators import user_passes_test

# Create your views here.




def registration(request):
    if request.user.is_authenticated:
        return redirect('bfc:myhome')
    else:
        context = {}
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(request, "Account created successfully, login now!!..")
                #messages.success(request, f'Your order has been placed successfully our correspondent will get contact you shortly')
                # login(request,account)
                return render(request,'account/registration_done.html',{'user': user})
            else:
                messages.warning(
                    request, "Error, unable to create account, please correct the errors below!!")
                form = RegistrationForm()
                context['registration_form'] = form
            return render(request, 'account/user-registration.html',context)
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request, 'account/user-registration.html', context)




def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("bfc:myhome")

    if request.method=="POST":
        if request.POST.get('email') == "" and request.POST.get('password') == "":
            messages.error(
                    request, "Error, please enter email and password!!")
           
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("bfc:myhome")
            else:
                messages.warning(request, "Account is not active, please contact admin!!..")
    else:
        pass      
  
    return render(request, "account/bfc.html",)


def login_view_required(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("bfc:myhome")

    if request.POST:
        
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("bfc:myhome")

    else:
        pass

    return render(request, "account/login_required.html",)


def account_view(request):
    initial_data={
                "email": request.user.email,
                "contact": request.user.contact,
                "firstName": request.user.firstName,
                "surName": request.user.surName,
                "country": request.user.country,
                "dob": request.user.dob,
            }
        
    if not request.user.is_authenticated:
        return redirect("account:login")

    context = {}
    if request.POST:
        form = UserUpdateForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()

    else:
        
        form = UserUpdateForm(initial = initial_data)
            

    context['account_form'] = form

    return render(request, "account/settings.html", context)


def account_fitler(request):
    items = Post.objects.filter(Post=request.user).order_by('-posted_date')
    context = {
        'items': items,
    }
    return render(request, 'account/account_settings.html', context)


def accountSettings(request):
    customer = request.user

    context = {'customer': customer,
               }
    return render(request, 'account/account_settings.html', context)
