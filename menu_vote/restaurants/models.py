from django.db import models

from menu_vote.base.models import TimeStampedModel


class Restaurant(TimeStampedModel):
    name = models.CharField(max_length=128)
