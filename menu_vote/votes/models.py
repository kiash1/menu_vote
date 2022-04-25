from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Subquery
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from menu_vote.votes.managers import VoteResultsManager

User = get_user_model()


class VoteResultMixin:
    def check_vote_results_published_for_date(self):
        if VoteResult.objects.filter(created_at_date=self.created_at_date).exists():
            raise ValidationError(
                {
                    "created_at": _("Vote results already published for this date.")
                }
            )

    def clean(self):
        super().clean()
        self.check_vote_results_published_for_date()


class Vote(VoteResultMixin, models.Model):
    created_at_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="votes")
    menu = models.ForeignKey("menus.Menu", on_delete=models.PROTECT, related_name="votes")

    class Meta:
        unique_together = ["user", "menu", "created_at_date"]

    def check_menu_uploaded_today(self):
        if not self.menu.created_at.date() == self.created_at_date:
            raise ValidationError(
                {
                    "menu": _("Please vote for a menu that was uploaded today.")
                }
            )

    def clean(self):
        super().clean()
        self.check_menu_uploaded_today()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.created_at_date = timezone.now().date()
        self.clean()
        super().save(force_insert, force_update, using, update_fields)


class VoteResult(VoteResultMixin, models.Model):
    created_at_date = models.DateField(auto_now_add=True, unique=True)
    menu = models.ForeignKey("menus.Menu", on_delete=models.PROTECT, related_name="vote_results")
    votes = models.IntegerField()

    objects = VoteResultsManager()

    def get_winning_menu(self):
        current_datetime = timezone.now()
        queryset = Vote.objects.filter(
            created_at_date=current_datetime.date()
        ).exclude(
            menu__restaurant__id__in=Subquery(
                VoteResult.objects.consecutive_winning_restaurants().values_list(
                    "menu__restaurant", flat=True
                )
            )
        ).values(
            "menu_id"
        ).annotate(
            menu_votes=Count("menu_id")
        )
        if not queryset:
            raise ValidationError(
                {
                    "menu": _("Unable to calculate today's winning votes.")
                }
            )
        return list(queryset)[0]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.created_at_date = timezone.now().date()
        self.clean()
        if not ((self.menu_id and self.votes) or self.id):
            winning_menu = self.get_winning_menu()
            self.menu_id = winning_menu.get("menu_id")
            self.votes = winning_menu.get("menu_votes", 0)
        super().save(force_insert, force_update, using, update_fields)
