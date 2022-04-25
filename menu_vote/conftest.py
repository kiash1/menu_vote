import base64

import pytest
from django.core.files.base import ContentFile
from factory import Faker
from rest_framework.test import APIClient

from menu_vote.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """
    Global DB access to all tests.
    :param db:
    :return:
    """
    pass


@pytest.fixture
def client():
    """
    better off using rest framework's api client instead of built in django test client for pytest
    since we'll be working with developing and testing apis
    :return:
    """
    return APIClient()


@pytest.fixture
def password():
    return Faker("word").generate()


@pytest.fixture
def user(password):
    return UserFactory(password=password)


@pytest.fixture
def superuser(user):
    user.is_superuser = True
    user.save()
    return user


@pytest.fixture
def auth_superuser_client(superuser, client):
    client.force_authenticate(superuser)
    return client


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user)
    return client
