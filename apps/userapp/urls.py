from apps.userapp.views import LoginView, SignupView
from django.urls import path


urlpatterns = [
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/signup/", SignupView.as_view(), name="signup"),
]
