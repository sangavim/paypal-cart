import unittest

def suite():   
    return unittest.TestLoader().discover("cart.tests", pattern="*.py")