from factory import DjangoModelFactory, SubFactory, Faker

from menu_vote.menus.models import Menu
from menu_vote.restaurants.tests.factories import RestaurantFactory


class MenuFactory(DjangoModelFactory):
    restaurant = SubFactory(RestaurantFactory)
    name = Faker("name")

    class Meta:
        model = Menu
