from django.urls import path, include

app_name = "api"
urlpatterns = [
    path('user/', include("backend.user.urls")),
    path('question/', include("backend.question.urls")),
    path('scoreboard/', include("backend.scoreboard.urls")),
    path('message/', include("backend.message.urls")),
]