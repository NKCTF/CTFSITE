from django.urls import path, include

from . import views


app_name = "user"
urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("logout/", views.log_out, name="logout"),
    path("auth_in/", views.user_auth_in, name="auth_in"),
    path("auth_back/", views.AuthLogin.as_view(), name="auth_back"),
    path("check/", include("backend.user.check.urls")),
    path("info/", include("backend.user.info.urls")),
    path("search/", include("backend.user.search.urls")),
    path("alter/", include("backend.user.alterdb.urls")),
]
