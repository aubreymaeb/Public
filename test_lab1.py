def increment_by_one(i):
    return i + 1

def test_answer():
    assert increment_by_one(1) == 2
    assert decrement_by_one(2) == 1

def decrement_by_one(x):
    return x - 1 