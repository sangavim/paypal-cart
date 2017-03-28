from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add_to_cart/(?P<product_id>[0-9]+)/(?P<quantity>[0-9]+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'^remove_from_cart/(?P<product_id>[0-9]+)/$', views.remove_from_cart, name="remove_from_cart"),
    url(r'^clear_cart/', views.clear_cart, name="clear_cart"),
    url(r'^cart/', views.get_cart, name="cart"),
    url(r'^buy/', views.buy_cart, name="buy"),
]

