from random import randint

import pytest
from django.urls import reverse
from django.utils import timezone

from menu_vote.menus.models import Menu
from menu_vote.menus.tests.factories import MenuFactory
from menu_vote.votes.models import Vote, VoteResult
from menu_vote.votes.tests.factories import VoteFactory, VoteResultFactory


class TestVoteAPI:

    url = reverse("api_v1:votes:create")

    @pytest.fixture
    def menu(self):
        return MenuFactory()

    def test_unauthenticated_vote_create(self, client):
        response = client.post(self.url)
        assert response.status_code == 403

    def test_vote_create(self, user, auth_client, menu):
        response = auth_client.post(self.url, data={"menu": menu.id})

        assert response.status_code == 201
        assert Vote.objects.filter(
            id=response.json().get("id"),
            user=user,
            menu_id=response.json().get("menu"),
            created_at_date=response.json().get("created_at_date")
        ).count() == 1

    def test_vote_multiple_times_same_day_different_menu(self, user, auth_client, menu):
        vote = VoteFactory(user=user)
        assert not vote.menu == menu

        response = auth_client.post(self.url, data={"menu": menu.id})

        assert response.status_code == 201
        assert Vote.objects.filter(
            id=response.json().get("id"),
            user=user,
            menu_id=response.json().get("menu"),
            created_at_date=response.json().get("created_at_date")
        ).count() == 1

    def test_vote_multiple_times_different_day(self, user, auth_client, menu):
        vote = VoteFactory(user=user)
        current_datetime = timezone.now()
        yesterday = current_datetime - timezone.timedelta(days=1)

        Vote.objects.filter(id=vote.id).update(created_at_date=yesterday.date())
        vote.refresh_from_db()

        assert vote.created_at_date == yesterday.date()

        response = auth_client.post(self.url, data={"menu": menu.id})

        assert response.status_code == 201
        assert Vote.objects.filter(
            id=response.json().get("id"),
            user=user,
            menu_id=menu.id,
            created_at_date=current_datetime.date()
        ).count() == 1

    def test_vote_for_menu_uploaded_yesterday(self, auth_client, menu):
        current_datetime = timezone.now()
        yesterday = current_datetime - timezone.timedelta(days=1)

        Menu.objects.filter(id=menu.id).update(created_at=yesterday)
        menu.refresh_from_db()

        assert menu.created_at == yesterday

        response = auth_client.post(self.url, data={"menu": menu.id})
        assert response.status_code == 400

    def test_vote_multiple_times_same_day_same_menu(self, user, auth_client, menu):
        VoteFactory(user=user, menu=menu)
        response = auth_client.post(self.url, data={"menu": menu.id})
        assert response.status_code == 400

    def test_vote_after_results_published(self, auth_client, menu):
        VoteResultFactory(menu=menu, votes=randint(10, 20))
        response = auth_client.post(self.url, data={"menu": menu.id})
        assert response.status_code == 400


class TestVoteResultsAPI:

    url = reverse("api_v1:vote_results:create_retrieve")

    @pytest.fixture
    def menu(self):
        return MenuFactory()

    def test_publish_vote_results(self, auth_client, menu):
        vote_count_1, vote_count_2 = [randint(10, 20) for _ in range(2)]
        winning_vote_count = randint(20, 30)
        VoteFactory.create_batch(size=vote_count_1)
        VoteFactory.create_batch(size=vote_count_2)
        VoteFactory.create_batch(size=winning_vote_count, menu=menu)

        response = auth_client.post(self.url)

        assert response.status_code == 201
        assert VoteResult.objects.filter(
            votes=winning_vote_count,
            menu=menu
        ).count() == 1

    def test_publish_multiple_results_on_same_day(self, auth_client):
        VoteResultFactory()
        response = auth_client.post(self.url)

        assert response.status_code == 400

    def test_get_published_results(self, auth_client, menu):
        vote_result = VoteResultFactory(menu=menu, votes=randint(10, 20))
        response = auth_client.get(self.url)

        assert response.status_code == 200
        assert response.json().get("id") == vote_result.id
