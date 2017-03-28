import paypalrestsdk
import logging

import json
from pprint import pprint

from . import models
from . import cart
from models import Cart, Item
from cart import Cart

class Payments:
    def __init__(self, request):
        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": "AesSQ-m769iI-g63hTgD5q-ik6FPdJ-WN9sZrXA3Uwd-sd1fB2Uf16cbfYkgO0VsAEotht3W0HM_S1im",
            "client_secret": "ENUEHvhTAkkcb425vWfqyNhvezQz3AC13JqRDNtVd00FDBTG9yodoCPgPSPXJmRuuwijNumM50Cnky4H"
        })
        self.payment_attr = {}
        self.payment_attr['intent'] = "sale"
        self.payment_attr['transactions'] = []
        self.payment_attr['payer'] = {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": {
                        "type": "visa",
                        "number": "4032030212895875",
                        "expire_month": "03",
                        "expire_year": "2022",
                        "cvv2": "874",
                        "first_name": "TestBuyer",
                        "last_name": "A"
                        }
                    }]
        }

    def buy(self, cart):
        total_price = 0
        item_data_list = []
        for item in cart.items():
            #pprint (vars(item))
            item_data = {}
            item_data['name'] = "item-" + str(item.object_id)
            item_data['sku'] = "sku-" + str(item.object_id)
            item_data['price'] = str(item.unit_price)
            item_data['quantity'] = item.quantity
            item_data['currency'] = "USD"
            item_data_list.append(item_data)
            total_price += (item.unit_price * item.quantity)
        self.payment_attr['transactions'] = [{
                "item_list": {
                    "items": item_data_list
                },
                "amount" : {
                    "total": str(total_price),
                    "currency": "USD" 
                },
                "description" : "Payment description"
        }]
        payment_attr_json=json.dumps(self.payment_attr)
        print(payment_attr_json)
        payment = paypalrestsdk.Payment(self.payment_attr)
        payement_create_response = payment.create()
        if payement_create_response:    
            print("Payment executed successfully: %s" % payment.id)
        else:
            print(payment.error)
        return payment
            
            
