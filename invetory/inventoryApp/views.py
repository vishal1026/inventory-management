# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from models import *

def index(request):
    return render(request, 'login.html')

def register(request):
    request
    if request.method == 'GET':
        return render(request, 'register.html', {'userExist':False})
    if request.method == 'POST':
        try:
            result = Inventory_users.objects.get(user_name=request.POST['userName'])
            return render(request, 'register.html', {'userExist':True})
        except:
            newUser = Inventory_users()
            newUser.first_name=request.POST['userName']
            newUser.last_name=request.POST['userName']
            newUser.user_name=request.POST['userName']
            newUser.password=request.POST['password']
            newUser.save()
    return render(request, 'login.html',{'userRegisteredSuccessfully':True, 'userExist':False})


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

