from django.contrib import admin
from .models import Robot
from orders.models import Order
# Register your models here.
admin.site.register(Robot)
admin.site.register(Order)

