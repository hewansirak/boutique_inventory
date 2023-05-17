from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', loginView.as_view(), name='login'),
    path('home/', Home, name='home'),
    path('admin_dash/', Home, name='admin_dashboard'),
    path('sales/', sales_view, name='sales'),
    path('stock_count/', sales_view, name='stock_count'),
    path('logout/', sales_view, name='logout'),
]