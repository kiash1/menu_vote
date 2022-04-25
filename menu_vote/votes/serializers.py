from django.core.exceptions import ValidationError
from django.db import IntegrityError

from rest_framework import serializers

from menu_vote.votes.models import Vote, VoteResult


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ["id", "menu", "user", "created_at_date"]
        read_only_fields = ["user", "created_at_date"]

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError as integrity_error:
            raise serializers.ValidationError(
                {
                    "menu": integrity_error
                }
            )
        except ValidationError as core_validation_error:
            raise serializers.ValidationError(core_validation_error.message_dict)


class VoteResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = VoteResult
        fields = ["id", "menu", "votes", "created_at_date"]
        read_only_fields = ["menu", "votes", "created_at_date"]

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except ValidationError as core_validation_error:
            raise serializers.ValidationError(core_validation_error.message_dict)
