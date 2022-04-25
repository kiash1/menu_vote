from rest_framework.generics import CreateAPIView

from menu_vote.base.permissions import IsAuthenticatedAndSuperUser
from menu_vote.users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedAndSuperUser]
    serializer_class = UserSerializer
