from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from Account.models import Account
from django.conf import settings
from django.http import HttpResponse
from django.core import files
from Account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            phone = form.cleaned_data.get('phone')
            Account = authenticate(email=email, password=raw_password)
            login(request, Account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'Account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context={}
    user=request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'Account/login.html', context)

def account_view(request, *args, **kwargs):
    context={}
    user_id = kwargs.get('user_id')
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.ImageURL
        context['hide_email'] = account.hide_email

        is_self = True
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
        context['is_self'] = is_self
        context['BASE_URL'] = settings.BASE_URL
        return render(request, 'Account/account.html', context)    

def edit_account_view(request, *args,**kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if account:
            context['profile_image'] = account.ImageURL
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account:view", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                initial={
                    "id": account.pk,
                    "email": account.email,
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                    "id": account.pk,
                    "email": account.email,
                    "username": account.username,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "Account/edit_account.html", context)
