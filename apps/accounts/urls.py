from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("entrar/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("salir/", auth_views.LogoutView.as_view(), name="logout"),
    path("registro/", views.SignupView.as_view(), name="signup"),
    path("panel/", views.DashboardView.as_view(), name="dashboard"),
]
