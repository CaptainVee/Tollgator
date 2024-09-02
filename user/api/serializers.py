from rest_framework import serializers
from courses.api.serializers import CourseSerializer
from user.models import Enrollment, User


class SocialMediaSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mode = serializers.CharField(required=True)


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ("id", "course", "last_video_watched", "completed", "completed_on")


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    signup_mode = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "email", "username", "is_instructor", "signup_mode"]
