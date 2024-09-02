from django.urls import path
from .views import VerifyTransactionAPIView

urlpatterns = [
    path("api/v1/verify/", VerifyTransactionAPIView.as_view(), name="api-verify-trasaction"),
]
