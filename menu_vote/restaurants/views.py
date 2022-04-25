from rest_framework.generics import ListCreateAPIView

from menu_vote.restaurants.models import Restaurant
from menu_vote.restaurants.serializers import RestaurantSerializer


class RestaurantListCreateAPIView(ListCreateAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
