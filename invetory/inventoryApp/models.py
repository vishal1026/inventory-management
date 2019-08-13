# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

userTypes = (
    ('admin','admin'),
    ('buyer','buyer'),
    )

class Inventory_users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique = True)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_active = models.BooleanField( default = True )
    user_type = models.CharField(choices=userTypes, max_length=5)

    class Meta:
        db_table = 'inventory_users'

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=20)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'products'

class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, related_name = 'purchase')
    user_id = models.ForeignKey(Inventory_users, related_name = 'purchase')
    quantity = models.IntegerField()

    class Meta:
        db_table = 'purchase'