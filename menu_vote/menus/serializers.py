from rest_framework import serializers

from menu_vote.menus.models import Menu


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "name"]
