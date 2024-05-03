from rest_framework import serializers
from courses.api.serializers import CourseSerializer
from user.models import Enrollment


class SocialMediaSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mode = serializers.CharField(required=True)


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ('id', 'course', 'last_video_watched', 'completed', 'completed_on')
