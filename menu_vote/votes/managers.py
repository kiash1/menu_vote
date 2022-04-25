from django.db import models
from django.db.models import Count
from django.utils import timezone


class VoteResultsManager(models.Manager):

    def consecutive_winning_restaurants(self):
        queryset = self.get_queryset().none()
        if self.get_queryset().count() > 1:
            current_datetime = timezone.now() - timezone.timedelta(days=2)
            queryset = self.get_queryset().filter(
                created_at_date__gte=current_datetime.date(),
                menu__restaurant=self.get_queryset().last().menu.restaurant
            ).values(
                "menu__restaurant"
            ).annotate(
                win_count=Count("menu__restaurant")
            ).filter(
                win_count=2
            )
        return queryset
