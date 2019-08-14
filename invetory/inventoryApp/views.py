# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
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
    print request.session.keys()
    print request.session.values()
    if 'user_id' in request.session and request.session['user_id']:
        return HttpResponseRedirect('/inventoryApp/profile/')

    if request.method == 'POST':
        try:
            result = Inventory_users.objects.get(user_name=request.POST['user_name'], password=request.POST['password'])
            if result:
                request.session['user_id'] = result.user_id
                request.session['user_name'] = result.user_name
                request.session['user_type'] = result.user_type
                return HttpResponseRedirect('/inventoryApp/profile/')
        except Inventory_users.DoesNotExist:
            return render(request, 'login.html',{'invalidcredential':True})
    return render(request, 'login.html',{'invalidcredential':False})


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/inventoryApp/')


def profile(request):
    if request.session['user_type'] == 'admin':
        productList = Products.objects.all()
        return render(request,'profile/admin/adminProfile.html', {'productList':productList})
    productList = Products.objects.exclude(quantity__lte = 0)
    return render(request,'profile/user/userProfile.html', {'productList':productList})


def productOperations(request):
    if request.method == 'POST':
        newProduct = Products()
        newProduct.product_name = request.POST['product_name']
        newProduct.quantity = int(request.POST['quantity'])
        newProduct.save()
        return render(request,'login.html')

@csrf_protect
def productPurchase(request):
    if request.method == 'POST':
        purchasedProduct = Products.objects.get(product_id = request.POST['product_id'])
        newPurchase = Purchase()
        newPurchase.product_id = purchasedProduct
        newPurchase.user_id = Inventory_users.objects.get( user_id = request.session['user_id'] )
        newPurchase.quantity = int(request.POST['quantity'])
        newPurchase.save()
        purchasedProduct.quantity = purchasedProduct.quantity - int(request.POST['quantity'])
        purchasedProduct.save()
        return render(request,'login.html')