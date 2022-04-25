from django.db import models

from menu_vote.base.models import TimeStampedModel


class Menu(TimeStampedModel):
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=128)
