from django.urls import path

from . import views

app_name="refresh_massage"
urlpatterns = [
    path("team/", views.refresh_team, name="team"),
]