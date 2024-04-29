from django.urls import path


from .views import profile, dashboard, progress, completed
from user.api.urls import urlpatterns as api_urlpatterns

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/in-progress/", progress, name="in-progress"),
    path("dashboard/completed/", completed, name="completed"),
]


htmx_urlpatterns = []

urlpatterns = urlpatterns + htmx_urlpatterns + api_urlpatterns
