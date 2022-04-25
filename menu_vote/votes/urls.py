from django.urls import path

from menu_vote.votes.views import VoteCreateAPIView, VoteResultCreateRetrieveAPIView

app_name = "votes"


urlpatterns = [
    path("", VoteCreateAPIView.as_view(), name="create")
]

vote_result_patterns = [
    path("", VoteResultCreateRetrieveAPIView.as_view(), name="create_retrieve")
]
