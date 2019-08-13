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
            result = Inventory_users.objects.get(user_name=request.POST['user_name'])
            return render(request, 'register.html', {'userExist':True})
        except:
            newUser = Inventory_users()
            newUser.first_name=request.POST['first_name']
            newUser.last_name=request.POST['last_name']
            newUser.user_name=request.POST['user_name']
            newUser.password=request.POST['password']
            newUser.save()
    return render(request, 'login.html',{'userRegisteredSuccessfully':True, 'userExist':False})


@csrf_protect
def login(request):
    if request.method == 'POST':
        try:
            result = Inventory_users.objects.get(user_name=request.POST['user_name'], password=request.POST['password'])
            if result:
                request.session['user_id'] = result.user_id
                request.session['user_name'] = result.user_name
                request.session['user_type'] = result.user_type
        except Inventory_users.DoesNotExist:
            return render(request, 'login.html',{'invalidcredential':True})
    return render(request,'profile/adminProfile.html')

def productOperations(request):
    if request.method == 'POST':
        newProduct = Products()
        newProduct.product_name = request.POST['product_name']
        newProduct.quantity = int(request.POST['quantity'])
        newProduct.save()
        return render(request,'login.html')