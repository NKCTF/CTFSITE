from django.urls import path, include

from .import views


app_name = "scoreboard"
urlpatterns = [
    path("user/", views.UserScore.as_view(), name="user"),
    path("team/", views.TeamScore.as_view(), name="team"),
    path("refresh/", include("backend.scoreboard.refresh.urls")),
]
