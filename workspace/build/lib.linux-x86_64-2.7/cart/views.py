from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from cart import Cart
from .models import Product
from .payments import Payments
from django.core.urlresolvers import reverse

def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(custom_id=product_id)
    cart = Cart(request)
    cart.add(product, product.price, quantity)
    print "ADD: %s - %s" % (product_id, quantity)
    # return render(request, 'index.html', {'cart' : cart})
    #return render(request, 'cart.html', {'cart' : cart})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_from_cart(request, product_id):
    product = Product.objects.get(custom_id=product_id)
    cart = Cart(request)
    cart.remove(product)
    print "REMOVE: %s" % (product_id) 
    #return render(request, 'index.html', {'cart' : cart})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def index(request):
    cart = Cart(request)
    return render(request, 'index.html', {'cart' : cart, 'status' : "Welcome! Companies on Sale!"})
    
def get_cart(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart' : cart})
    
def buy_cart(request):
    cart = Cart(request)
    paypal_payments = Payments(request)
    payment_id = paypal_payments.buy(cart)
    if payment_id == -1:
        return render(request, 'index.html', {'cart' : cart, 'status' : "Error Buying the Cart! Please try again!"})
        #url = reverse(request.META.get('HTTP_REFERER'), kwargs={'status' : "Error Buying the Cart! Please try again! Reason: "})
        #return HttpResponseRedirect(url)
        #return render(request, 'error.html')
    else:
        cart.clear()
        return render(request, 'index.html' ,{'cart' : cart, 'status' : payment_id})
        #url = reverse(request.META.get('HTTP_REFERER'),kwargs={'status' : payment_id})
        #return HttpResponseRedirect(url)
        #return render(request, 'success.html')
    
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
#   cart = [{'item1': "g", 'item2': 2, 'item3': 100}] 
# return render(request, 'cart.html', {'cart': cart})