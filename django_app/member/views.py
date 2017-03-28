from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render


def login_fbv(request):
    # return HttpResponse('login view')

    context = {

    }
    return render(request, 'member/login.html', context)