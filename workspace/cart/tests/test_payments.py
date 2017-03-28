from decimal import Decimal
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser

import paypalrestsdk
import logging

class PayPalPaymentsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}
        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": "AesSQ-m769iI-g63hTgD5q-ik6FPdJ-WN9sZrXA3Uwd-sd1fB2Uf16cbfYkgO0VsAEotht3W0HM_S1im",
            "client_secret": "ENUEHvhTAkkcb425vWfqyNhvezQz3AC13JqRDNtVd00FDBTG9yodoCPgPSPXJmRuuwijNumM50Cnky4H"
        })

    def test_paypal_rest_sdk_payment(self):
        print("Testing PayPal payment execute!")
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
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
                },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item1",
                        "sku": "item1",
                        "price": "0.99",
                        "currency": "USD",
                        "quantity": 1
                        }, {
                        "name": "item2",
                        "sku": "item2",
                        "price": "0.99",
                        "currency": "USD",
                        "quantity": 1
                        }]
                    },
                "amount": {
                    "total": "1.98",
                    "currency": "USD" 
                    },
                "description": "This is the payment transaction description."
            }]
        })
        payement_create_response = payment.create()
        if payement_create_response:    
            print("Payment created successfully: %s" % payment.id)
        else:
            print(payment.error)
            
            
    def test_paypal_rest_sdk_payment_history(self):
        try:
            payment_history = paypalrestsdk.Payment.all()
            print(payment_history.payments)
        except:
            import sys
            e = sys.exc_info()[1]
            print("Couldn't fetch payments history: %s" % e)    