import pytest
from app.calculations import add 

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 1, 2), 
    (2, 2, 4), 
    (3, 3, 6)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected