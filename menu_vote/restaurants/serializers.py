from rest_framework import serializers

from menu_vote.restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ["id", "name", "created_at", "updated_at"]
