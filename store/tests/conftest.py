import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from store.models import Collection
from model_bakery import baker 

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate

