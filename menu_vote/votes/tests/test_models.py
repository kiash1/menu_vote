from random import randint

from django.utils import timezone

from menu_vote.menus.tests.factories import MenuFactory
from menu_vote.restaurants.tests.factories import RestaurantFactory
from menu_vote.votes.models import VoteResult
from menu_vote.votes.tests.factories import VoteFactory, VoteResultFactory


class TestVoteResultModel:

    def update_vote_result_created_at(self, vote_result_id_list, new_created_at):
        VoteResult.objects.filter(id__in=vote_result_id_list).update(created_at_date=new_created_at)

    def test_calculate_winning_menu(self):
        menu_1, menu_2, menu_3 = MenuFactory.create_batch(size=3)
        VoteFactory.create_batch(size=10, menu=menu_1)
        VoteFactory.create_batch(size=9, menu=menu_2)
        VoteFactory.create_batch(size=8, menu=menu_3)

        vote_result = VoteResult.objects.create()

        assert vote_result.menu == menu_1
        assert vote_result.votes == 10

    def test_calculate_winning_menu_with_previous_consecutive_winners(self):
        restaurant = RestaurantFactory()
        menu_1, menu_2 = MenuFactory.create_batch(size=2, restaurant=restaurant)
        menu_3 = MenuFactory()

        current_day = timezone.now()
        day_before_yesterday = current_day - timezone.timedelta(days=2)
        yesterday = current_day - timezone.timedelta(days=1)
        votes = randint(10, 20)

        # construct previous winners
        vote_result_1 = VoteResultFactory(menu=menu_1, votes=votes)
        self.update_vote_result_created_at([vote_result_1.id], day_before_yesterday)
        vote_result_1.refresh_from_db()

        assert vote_result_1.created_at_date == day_before_yesterday.date()

        vote_result_2 = VoteResultFactory(menu=menu_2, votes=votes)
        self.update_vote_result_created_at([vote_result_2.id], yesterday)
        vote_result_2.refresh_from_db()

        assert vote_result_2.created_at_date == yesterday.date()

        # cast votes for current date
        VoteFactory.create_batch(size=10, menu=menu_1)
        VoteFactory.create_batch(size=9, menu=menu_2)
        VoteFactory.create_batch(size=8, menu=menu_3)

        vote_result = VoteResult.objects.create()

        assert vote_result.menu == menu_3
        assert vote_result.votes == 8

    def test_calculate_winning_menu_with_previous_non_consecutive_winner(self):
        menu_1, menu_2, menu_3 = MenuFactory.create_batch(size=3)

        current_day = timezone.now()
        day_before_yesterday = current_day - timezone.timedelta(days=2)
        yesterday = current_day - timezone.timedelta(days=1)
        votes = randint(10, 20)

        # construct previous winners
        vote_result_1 = VoteResultFactory(menu=menu_1, votes=votes)
        self.update_vote_result_created_at([vote_result_1.id], day_before_yesterday)
        vote_result_1.refresh_from_db()

        assert vote_result_1.created_at_date == day_before_yesterday.date()

        vote_result_2 = VoteResultFactory(menu=menu_2, votes=votes)
        self.update_vote_result_created_at([vote_result_2.id], yesterday)
        vote_result_2.refresh_from_db()

        assert vote_result_2.created_at_date == yesterday.date()

        VoteFactory.create_batch(size=10, menu=menu_1)
        VoteFactory.create_batch(size=9, menu=menu_2)
        VoteFactory.create_batch(size=8, menu=menu_3)

        vote_result = VoteResult.objects.create()

        assert vote_result.menu == menu_1
        assert vote_result.votes == 10
