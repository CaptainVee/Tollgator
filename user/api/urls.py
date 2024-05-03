from django.urls import path, include
from .views import (
    SocialRegistrationView,
    CustomLoginView,
    CustomRegisterView,
    UserEnrollmentView,
)


urlpatterns = [
    path("api/v1/social/", SocialRegistrationView.as_view(), name="social-login-api"),
    path("api/v1/register/", CustomRegisterView.as_view(), name="registeration-api"),
    path("api/v1/login/", CustomLoginView.as_view(), name="login-api"),
    path("api/v1/my-courses/", UserEnrollmentView.as_view(), name="my-courses"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
]
