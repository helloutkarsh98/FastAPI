import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    # assert 2 == 3


def test_is_instance():
    assert isinstance('This is string', str)
    assert not isinstance('10', int)
    assert isinstance(10, int)



def test_boolean():
    assert (10==10) is True
    # assert 10 > 7 is False



def test_type():
    assert type(10) is int
    assert type('Hello') is str
    # assert type('World') is not str



def test_greater_than_and_less_than():
    assert 10 > 7
    # assert 4 > 7



def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False, False]

    # assert 7 in num_list
    assert 10 not in num_list
    assert all(num_list)
    assert not any(any_list)




class Student:
    def __init__(self, first_name:str, last_name:str, major:str, year:int):
        self.first_name = first_name
        self.last_name= last_name
        self.major = major
        self.year = year


@pytest.fixture
def default_employee():
    return Student('Pappu', 'Gandhi', 'Computer Science', 3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == 'Pappu', 'First name should be Pappu'
    assert default_employee.last_name == 'Gandhi', 'Last name should be Gandhi'
    assert default_employee.major == "Computer Science", 'Major is computer science'
    assert default_employee.year == 3, 'year is 3'
    
    