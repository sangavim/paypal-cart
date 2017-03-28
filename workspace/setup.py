#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name='paypal-cart',
        version='0.1',
        description='Django shopping cart with PayPal integration!',
        maintainer='Sangavi Muthuvel',
        maintainer_email='sangavi.cs88@gmail.com',
        license="GNU v3",
        url='',
        packages=['cart', 'cart.migrations'],
        classifiers=[
            "Development Status :: 1 - Evolving",
            "Framework :: Django",
            "Programming Language :: Python",
        ],
     )