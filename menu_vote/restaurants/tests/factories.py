from factory import DjangoModelFactory, Faker

from menu_vote.restaurants.models import Restaurant


class RestaurantFactory(DjangoModelFactory):
    name = Faker("first_name")

    class Meta:
        model = Restaurant
