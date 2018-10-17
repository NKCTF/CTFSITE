from django.urls import path,include

from . import views


app_name = "massage"
urlpatterns = [
    path("mail_box/", views.MailBox.as_view(), name="mail_box"),
    path("refresh/", include("backend.message.refresh.urls")),
]
