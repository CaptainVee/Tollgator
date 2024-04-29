from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

# from rest_framework.renderers import JSONRenderer
# from rest_framework.authtoken.models import Token
# from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_password
from .serializers import SocialMediaSerializer
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class SocialRegistrationView(CreateAPIView):
    """
    Api for registering users via social media.
    """

    permission_classes = (AllowAny,)
    serializer_class = SocialMediaSerializer

    def make_user(self, instance):
        password = generate_password()
        user = User.objects.create(
            name=f"{instance['first_name']} {instance['last_name']}",
            email=instance["email"].replace(" ", "").lower(),
            username=instance["email"].replace(" ", "").lower().split("@")[0],
        )
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.data
            try:
                user = User.objects.get(
                    email=instance["email"].replace(" ", "").lower()
                )
                refresh = RefreshToken.for_user(user)
                content = {
                    "active": user.is_active,
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    "full_name": user.get_full_name,
                }
                return Response(content, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                user = self.make_user(instance)
                refresh = RefreshToken.for_user(user)
                content = {
                    "active": user.is_active,
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    "full_name": user.get_full_name,
                }
                return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        # Get the username and password from the request data
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if a user with the provided username exists
        try:
            user = User.objects.get(email=email)

            # Check if the user's signup_mode is "Social"
            if user.signup_mode == "Google":
                return Response(
                    {"detail": "Please use the social login method."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Authenticate the user with the provided password
            user = authenticate(email=email, password=password)

            # If authentication fails, return an error response
            if not user:
                return Response(
                    {"message": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST
                )

            # If authentication is successful, log in the user and return a success response
            refresh = RefreshToken.for_user(user)
            content = {
                "active": user.is_active,
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "full_name": user.get_full_name,
            }
            return Response(content, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        # Check if the signup_mode field is provided in the request data
        signup_mode = self.request.data.get("signup_mode")

        # If signup_mode is not provided, default to "Email"
        # if not signup_mode:
        #     signup_mode = "Email"

        # If signup_mode is "Social", return an error response
        if signup_mode == "Social":
            return Response(
                {"detail": "Social sign-up is not allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call the parent's perform_create method to create the user
        super().perform_create(serializer)

        # If registration is successful, generate JWT tokens and return them
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        content = {
            "active": user.is_active,
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "full_name": user.get_full_name,
        }
        return Response(content, status=status.HTTP_201_CREATED)
