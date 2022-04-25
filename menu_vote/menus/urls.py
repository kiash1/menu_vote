from django.urls import path

from menu_vote.menus.views import MenuListCreateAPIView

app_name = "menus"

urlpatterns = [
    path("", MenuListCreateAPIView.as_view(), name="list_create")
]
