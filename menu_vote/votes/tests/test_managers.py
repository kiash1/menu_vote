from random import randint

from django.utils import timezone

from menu_vote.menus.tests.factories import MenuFactory
from menu_vote.restaurants.tests.factories import RestaurantFactory
from menu_vote.votes.models import VoteResult
from menu_vote.votes.tests.factories import VoteResultFactory


class TestVoteResultManager:

    def update_vote_result_created_at(self, vote_result_id_list, new_created_at):
        VoteResult.objects.filter(id__in=vote_result_id_list).update(created_at_date=new_created_at)

    def test_get_consecutive_winning_restaurant(self):
        votes = randint(10, 50)
        restaurant = RestaurantFactory()
        menu_1, menu_2 = MenuFactory.create_batch(size=2, restaurant=restaurant)

        current_day = timezone.now()
        day_before_yesterday = current_day - timezone.timedelta(days=2)
        yesterday = current_day - timezone.timedelta(days=1)

        vote_1 = VoteResultFactory(menu=menu_1, votes=votes)
        self.update_vote_result_created_at([vote_1.id], day_before_yesterday)
        vote_1.refresh_from_db()

        assert vote_1.created_at_date == day_before_yesterday.date()

        vote_2 = VoteResultFactory(menu=menu_2, votes=votes)
        self.update_vote_result_created_at([vote_2.id], yesterday)
        vote_2.refresh_from_db()

        assert vote_2.created_at_date == yesterday.date()

        assert list(
            VoteResult.objects.consecutive_winning_restaurants()
        ) == [{
            "menu__restaurant": restaurant.id,
            "win_count": 2
        }]
