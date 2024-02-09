from django.shortcuts import render
from Account.models import Account

def home_view(request):
    user_id = request.user.id
    context={}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass
    return render(request, 'home/index.html', context)

def project_view(request):
    user_id = request.user.id
    context={}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass
    return render(request, 'home/project.html', context)
