from _pytest.python_api import raises
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from factory import Faker
from factory.fuzzy import FuzzyInteger
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import RefreshToken


class TestToken:
    obtain_pair_url = reverse("api_v1:user:token_obtain_pair")
    obtain_refresh_url = reverse("api_v1:user:token_refresh")

    def validate_access_token(self, access_token, user):
        access_token_payload = token_backend.decode(access_token, True)
        assert access_token_payload.get("token_type", "") == "access"
        assert access_token_payload.get("user_id", "") == user.id

    def validate_refresh_token(self, refresh_token, user):
        refresh_token_payload = token_backend.decode(refresh_token, True)
        assert refresh_token_payload.get("token_type", "") == "refresh"
        assert refresh_token_payload.get("user_id", "") == user.id

    def test_token_obtain_pair(self, client, user, password):
        response = client.post(
            self.obtain_pair_url, {"username": user.username, "password": password}
        )
        assert response.status_code == 200
        access_token = response.data.get("access", "")
        refresh_token = response.data.get("refresh", "")
        self.validate_access_token(access_token, user)
        self.validate_refresh_token(refresh_token, user)

    def test_token_obtain_refresh(self, client, user):
        refresh_token = str(RefreshToken.for_user(user))
        response = client.post(self.obtain_refresh_url, {"refresh": refresh_token})
        assert response.status_code == 200
        access_token = response.json().get("access", "")
        new_refresh_token = response.json().get("refresh", "")
        self.validate_access_token(access_token, user)
        self.validate_refresh_token(new_refresh_token, user)

        with raises(TokenError) as token_error:
            RefreshToken(refresh_token).check_blacklist()
            assert token_error

    def test_inactive_user_token_obtain_pair(self, client, user, password):
        user.is_active = False
        user.save()
        response = client.post(
            self.obtain_pair_url, {"username": user.username, "password": password}
        )
        assert response.status_code == 401

    def test_token_obtain_pair_with_invalid_credentials(self, client, user):
        response = client.post(
            self.obtain_pair_url, {"username": user.username, "password": "invalid"}
        )
        assert response.status_code == 401


class TestRegistration:

    url = reverse("api_v1:user:register")

    def test_user_register(self, auth_superuser_client, django_user_model):
        data = {
            "username": Faker("first_name").generate(),
            "password": Faker("password", length=FuzzyInteger(low=8, high=20).fuzz()).generate()
        }

        response = auth_superuser_client.post(self.url, data=data)
        assert response.status_code == 201
        queryset = django_user_model.objects.filter(
            id=response.json().get("id"),
            username__exact=response.json().get("username", ""),
            is_active=True
        )
        assert queryset.count() == 1  # check only single record exists
        # check user entered user password has been hashed and set
        assert check_password(data.get("password", ""), queryset.first().password)

    def test_user_register_as_non_superuser(self, auth_client):
        response = auth_client.post(self.url)
        assert response.status_code == 403

    def test_user_register_as_unauthenticated_user(self, client):
        response = client.post(self.url)
        assert response.status_code == 403

    def test_user_register_fail_password_validation(self, auth_superuser_client):
        data = {
            "username": Faker("first_name").generate(),
            "password": str(FuzzyInteger(low=10000000, high=99999999).fuzz())
        }

        response = auth_superuser_client.post(self.url, data=data)
        assert response.status_code == 400
        assert response.json().get("password", "") == ["This password is entirely numeric."]
