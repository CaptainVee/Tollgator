from django.urls import path
from courses.api.views import TopEnrolledCoursesView, CourseDetailAPIView


urlpatterns = [
    path("api/v1/courses/", TopEnrolledCoursesView.as_view(), name="api-course-home"),
    path("api/v1/courses/<str:slug>/", CourseDetailAPIView.as_view(), name="api-course-details"),
]
