from django.urls import path
from .views import SocialRegistrationView, CustomLoginView, CustomRegisterView


urlpatterns = [
    path("api/v1/social/", SocialRegistrationView.as_view(), name="social-login-api"),
    path("api/v1/register/", CustomRegisterView.as_view(), name="registeration-api"),
    path("api/v1/login/", CustomLoginView.as_view(), name="login-api"),
]
