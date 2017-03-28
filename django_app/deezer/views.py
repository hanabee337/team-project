from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    # return HttpResponse('index')
    return redirect('member:login')