from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="kitchen/registration/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="kitchen/registration/logged_out.html"
        ),
        name="logout",
    ),
]

app_name = "accounts"
