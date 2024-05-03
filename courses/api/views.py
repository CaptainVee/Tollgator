from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count
from courses.models import Course, Category, Video
from .serializers import CourseSerializer, CategorySerializer, CourseDetailSerializer
import random


class Home(APIView):
    """
    Renders the landing page for unauthenticated users but renders
    courses list page for authenticated users
    """

    paginate_by = 5

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            courses_queryset = Course.objects.filter(is_private=False).order_by(
                "-updated_at"
            )
            courses_serializer = CourseSerializer(courses_queryset, many=True)
        else:
            courses_queryset = list(Course.objects.filter(is_private=False))
            try:
                courses = random.sample(courses_queryset, 4)
            except ValueError:
                courses = Course.objects.filter(is_private=False)[:4]
            courses_serializer = CourseSerializer(courses, many=True)

        return Response(courses_serializer.data)


# class TopRatedCoursesView(APIView):
#     def get(self, request):
#         # Get all categories
#         categories = Category.objects.all()

#         # Initialize an empty dictionary to store top-rated courses per category
#         top_rated_courses = {}
#         # breakpoint()
#         for category in categories:
#             # Filter courses by category and calculate average rating
#             courses = Course.objects.filter(category=category)
#             course_ratings = CourseRating.objects.filter(course__in=courses).aggregate(
#                 avg_rating=Avg("value")
#             )

#             # Check if there are any ratings for the category
#             if course_ratings["avg_rating"] is not None:
#                 print("this is avg rating", course_ratings)
#                 # Filter top 3 courses with highest average rating
#                 top_courses_by_category = (
#                     courses.annotate(average_rating=Avg("course_rating__value"))
#                     .order_by("-average_rating")[:3]
#                 )
#                 top_rated_courses[category.name] = CourseSerializer(
#                     top_courses_by_category, many=True
#                 ).data
#             else:
#                 print("no course ratings")
#                 # If no ratings, include an empty list for the category
#                 top_rated_courses[category.name] = CourseSerializer(
#                         courses.order_by("-created_at")[:3], many=True
#                     ).data
#         return Response(top_rated_courses, status=status.HTTP_200_OK)


class TopEnrolledCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all categories ordered by course count (descending)
        top_categories = Category.objects.annotate(
            course_count=Count("course")
        ).order_by("-course_count")[:5]

        continue_watching = request.user.user_dashboard.courses.all()[:5]

        serialized_courses_with_progress = []

        for course in continue_watching:
            # Calculate completed video count for the current course
            completed_count = Video.objects.filter(
                course=course, watchtime__finished_video=True
            ).count()

            # Calculate progress for the current course
            if course.video_count > 0:
                progress = (completed_count / course.video_count) * 100
            else:
                progress = 0  # Avoid division by zero

            # Serialize the course data
            serialized_course = CourseSerializer(course).data

            # Add progress information to the serialized course data
            serialized_course["progress"] = progress

            # Append the serialized course with progress to the list
            serialized_courses_with_progress.append(serialized_course)

        serializer = CategorySerializer(top_categories, many=True)
        context = {
            "continue_watching": serialized_courses_with_progress,
            "categories": serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)

        # Initialize an empty list to store top category data
        # top_enrolled_categories = []

        # for category in top_categories:
        #     # Generate a unique UUID for the category

        #     # Filter courses by the current category
        #     courses = Course.objects.filter(category=category)

        #     # Annotate courses with enrollment count using a subquery
        #     top_courses_by_category = (
        #         courses.annotate(enrolled_users=Count("enrollment__user_dashboard"))
        #         .order_by("-enrolled_users")[:3]
        #     )

        #     # Serialize the top courses
        #     serialized_courses = CourseSerializer(top_courses_by_category, many=True).data

        #     # Create a dictionary for the current category
        #     category_data = {
        #         "category": category.name,
        #         "courses": serialized_courses,
        #     }


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = "slug"
