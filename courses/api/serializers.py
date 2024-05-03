from rest_framework import serializers
from courses.models import Course, Category, Lesson, CourseRating, Video
from instructor.api.serializers import InstructorSerializer
from user.models import Enrollment
from django.db.models import Count


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "title", "duration_seconds"]


class LessonSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = "__all__"

    def get_videos(self, obj):
        videos = obj.videos
        serializers = VideoListSerializer(videos, many=True)
        return serializers.data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    author = InstructorSerializer(source='author.instructor', read_only=True)
    enrolled_users = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response[
            "content"
        ] = instance.content.html  # this is becouse content is a quillfield
        return response

    def get_enrolled_users(self, obj):
        # Get the number of enrolled users for the current course object
        enrolled_count = Enrollment.objects.filter(course__id=obj.id).count()
        return enrolled_count

    def get_lessons(self, obj):
        lessons = obj.lessons
        serializers = LessonSerializer(lessons, many=True)
        return serializers.data

    def get_reviews(self, obj):
        reviews = obj.course_rating.all().order_by("created_at")
        serializers = ReviewSerializer(reviews, many=True)
        return serializers.data


class CourseSerializer(serializers.ModelSerializer):
    enrolled_users = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    users_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "enrolled_users",
            "created_at",
            "updated_at",
            "title",
            "brief_description",
            "slug",
            "thumbnail",
            "thumbnail_url",
            "total_watch_time",
            "price",
            'avg_rating',
            "users_enrolled",
        ]

    def get_enrolled_users(self, obj):
        # Get the number of enrolled users for the current course object
        enrolled_count = Enrollment.objects.filter(course__id=obj.id).count()
        return enrolled_count

    def get_avg_rating(self, obj):
        return obj.get_average_rating()

    def get_users_enrolled(self, obj):
        return obj.get_enrollment_count()


class CategorySerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "courses"]

    def get_courses(self, obj):
        courses = Course.objects.filter(category=obj)

        top_courses_by_category = courses.annotate(
            enrolled_users=Count("enrollment__user_dashboard")
        ).order_by("-enrolled_users")[:3]
        serialized_courses = CourseSerializer(top_courses_by_category, many=True).data

        return serialized_courses
