# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from models import *

def index(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        return HttpResponse("User exist")
    return HttpResponse("Last")


@csrf_protect
def login(request):
    if request.method == 'POST':
        try:
            result = Inventory_users.objects.get(user_name=request.POST['userName'], password=request.POST['password'])
            print result
            if result:
                request.session['user_id'] = result.user_id
                request.session['user_name'] = result.user_name
                request.session['user_type'] = result.user_type
        except Inventory_users.DoesNotExist:
            return render(request, 'login.html',{'invalidcredential':True})
    return HttpResponse("User exist")

