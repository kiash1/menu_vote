from django.utils import timezone
from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404

from menu_vote.votes.models import VoteResult
from menu_vote.votes.serializers import VoteSerializer, VoteResultSerializer


class VoteCreateAPIView(CreateAPIView):
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class VoteResultCreateRetrieveAPIView(CreateAPIView, RetrieveAPIView):
    serializer_class = VoteResultSerializer

    def get_object(self):
        return get_object_or_404(
            VoteResult, created_at_date=timezone.now().date()
        )

    def perform_create(self, serializer):
        serializer.save()
