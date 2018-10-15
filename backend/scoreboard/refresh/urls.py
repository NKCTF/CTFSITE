from django.urls import path

from . import views

app_name = "refresh"
urlpatterns = [
    path("all/", views.rAll.as_view(), name="all"),
    path("user/", views.rUser.as_view(), name="user"),
    path("board/", views.rBoard.as_view(), name="board"),
]