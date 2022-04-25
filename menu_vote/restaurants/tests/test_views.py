from random import randint

from django.urls import reverse
from factory import Faker

from menu_vote.restaurants.models import Restaurant
from menu_vote.restaurants.tests.factories import RestaurantFactory


class TestRestaurant:

    url = reverse("api_v1:restaurants:list_create")

    def test_get_restaurants(self, auth_client):
        size = randint(2, 5)
        restaurants = RestaurantFactory.create_batch(size=size)

        response = auth_client.get(self.url)

        assert response.status_code == 200
        assert response.json().get("count", 0) == size

        results = response.json().get("results", [])
        assert [result.get("id") for result in results] == [restaurant.id for restaurant in restaurants]

    def test_create_restaurant(self, auth_client):
        data = {
            "name": Faker("name").generate()
        }

        response = auth_client.post(self.url, data=data)
        assert response.status_code == 201
        assert response.json().get("name", "") == data.get("name", "")
        assert Restaurant.objects.filter(
            name__exact=data.get("name", ""),
            id=response.json().get("id")
        ).count() == 1

    def test_unauthenticated_get_restaurant(self, client):
        response = client.get(self.url)
        assert response.status_code == 403

    def test_unauthenticated_create_restaurant(self, client):
        response = client.post(self.url, data={})
        assert response.status_code == 403
