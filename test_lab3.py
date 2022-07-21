import pytest

class Calculator:
    def add(self, a, b):
        return a + b
        

def test_add():
    assert calc.add(1,1) ==2
    assert calc.add(1.0,2.5) == 3.5
    assert calc.add(0,0) == 0
    assert calc.add(-5,-6) == -11
    
calc = Calculator()

print(calc.add(1, 1))