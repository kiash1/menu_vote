from rest_framework.generics import ListCreateAPIView

from menu_vote.menus.filters import MenuFilter
from menu_vote.menus.models import Menu
from menu_vote.menus.serializers import MenuSerializer


class MenuListCreateAPIView(ListCreateAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    filterset_class = MenuFilter
