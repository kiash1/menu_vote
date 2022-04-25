from factory import DjangoModelFactory, SubFactory
from factory.fuzzy import FuzzyInteger

from menu_vote.menus.tests.factories import MenuFactory
from menu_vote.users.tests.factories import UserFactory
from menu_vote.votes.models import Vote, VoteResult


class VoteFactory(DjangoModelFactory):
    menu = SubFactory(MenuFactory)
    user = SubFactory(UserFactory)

    class Meta:
        model = Vote


class VoteResultFactory(DjangoModelFactory):
    menu = SubFactory(MenuFactory)
    votes = FuzzyInteger(low=20, high=100)

    class Meta:
        model = VoteResult
