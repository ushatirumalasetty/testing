from django.test import TestCase
from .models import *
import pytest

from freezegun import freeze_time
import datetime
import unittest


@freeze_time("2012-01-14")
def test():
    assert datetime.datetime.now() == datetime.datetime(2012, 1, 14)

# Or a unittest TestCase - freezes for every test, from the start of setUpClass to the end of tearDownClass

@freeze_time("1955-11-12")
class MyTests(unittest.TestCase):
    def test_the_class(self):
        assert datetime.datetime.now() == datetime.datetime(1955, 11, 12)

# Or any other class - freezes around each callable (may not work in every case)

@freeze_time("2012-01-14")
class Tester(object):
    def test_the_class(self):
        assert datetime.datetime.now() == datetime.datetime(2012, 1, 14)
        
        
@pytest.mark.django_db
def test_create_a_post_valid():
  user_id=User.objects.get(id=1)
  posted_at=datetime.datetime.now()
  assert posted_at==test()
  
  
