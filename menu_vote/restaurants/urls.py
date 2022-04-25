from django.urls import path

from menu_vote.restaurants.views import RestaurantListCreateAPIView

app_name = "restaurants"

urlpatterns = [
    path("", RestaurantListCreateAPIView.as_view(), name="list_create")
]
