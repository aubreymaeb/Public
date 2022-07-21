import pytest

class Calculator:
    def __init__(self, name):
        self.name = name
    def add(self, a, b):
        return a + b

@pytest.fixture
def base_calculator():
    return Calculator("Base Calculator")

def test_lab4_test1(base_calculator):
    print("#1 This calculator's name is " + base_calculator.name)
    
    # Changing calculator's name
    base_calculator.name = "Changed Calculator"
    print("#1 This calculator's name is " + base_calculator.name)
    
    assert True

def test_lab4_test2(base_calculator):
    print("#2 This calculator's name is " + base_calculator.name)
    
    assert True

    
def test_operations():
    assert calc.add(1,1) == 2
    assert calc.subtract(3,2) == 1
    assert calc.multiply(2,3) == 6