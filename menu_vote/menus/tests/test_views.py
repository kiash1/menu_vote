from random import randint

import pytest
from django.urls import reverse
from django.utils import timezone
from factory import Faker

from menu_vote.menus.models import Menu
from menu_vote.menus.tests.factories import MenuFactory
from menu_vote.restaurants.tests.factories import RestaurantFactory


class TestMenu:

    url = reverse("api_v1:menus:list_create")

    @pytest.fixture
    def restaurant(self):
        return RestaurantFactory()

    def test_menu_create(self, auth_client, restaurant):

        data = {
            "name": Faker("first_name").generate(),
            "restaurant": restaurant.id
        }

        response = auth_client.post(self.url, data=data)

        response_json = response.json()
        assert response.status_code == 201
        assert Menu.objects.filter(
            id=response_json.get("id"),
            name=response_json.get("name", ""),
            restaurant_id=restaurant.id
        ).count() == 1

    def test_menu_list(self, auth_client):
        size = randint(2, 5)
        menus = MenuFactory.create_batch(size=size)

        response = auth_client.get(self.url)

        assert response.status_code == 200
        assert response.json().get("count", 0) == size
        results = response.json().get("results", [])
        assert [result.get("id") for result in results] == [menu.id for menu in menus]

    def test_menu_filter(self, auth_client):
        past_datetime = timezone.now() - timezone.timedelta(days=3)
        past_menu = MenuFactory()
        Menu.objects.filter(id=past_menu.id).update(created_at=past_datetime)
        past_menu.refresh_from_db()

        MenuFactory()

        # assert we have two objects in db
        assert Menu.objects.count() == 2

        response = auth_client.get(self.url, data={"upload_date": past_datetime.strftime("%Y-%m-%d")})
        assert response.status_code == 200
        assert response.json().get("count", 0) == 1

        results = response.json().get("results", [])
        past_menu_data = results.pop()

        assert past_menu_data.get("id") == past_menu.id

    def test_get_current_date_menus_without_upload_date_filter(self, auth_client):
        past_datetime = timezone.now() - timezone.timedelta(days=3)
        past_menu = MenuFactory()
        Menu.objects.filter(id=past_menu.id).update(created_at=past_datetime)
        past_menu.refresh_from_db()

        present_menu = MenuFactory()

        response = auth_client.get(self.url)
        assert response.status_code == 200
        assert response.json().get("count", 0) == 1

        results = response.json().get("results", [])
        past_menu_data = results.pop()

        assert past_menu_data.get("id") == present_menu.id

    def test_unauthenticated_create_menu(self, client):
        response = client.post(self.url)
        assert response.status_code == 403

    def test_unauthenticated_get_menu(self, client):
        response = client.post(self.url)
        assert response.status_code == 403
