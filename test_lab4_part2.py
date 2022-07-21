import pytest

class Calculator:
    def add(self, a, b):
        return a + b
    def subtract(self,c,d):
        return c-d
    def multiply(self,e,f):
        return e*f
calc=Calculator()

def test_operations():
    #assert calc.add(1,1) == 2
    assert calc.subtract(3,2) == 1
    assert calc.multiply(2,3) == 6
