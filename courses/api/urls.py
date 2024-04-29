from django.urls import path
from courses.api.views import (

)
urlpatterns = [
    path("", Home.as_view(), name="course-home"),
    # path("courses/", CourseListView.as_view(), name="course-list"),
    path("course/new/", CourseCreateView.as_view(), name="course-create"),
    path(
        "course/new/playlist",
        course_create_playlist_view,
        name="course-create-playlist",
    ),
    path(
        "course/<slug:course_slug>/details",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
    path("course/<int:pk>/update/", CourseUpdateView, name="course-update"),
    path("course/<int:pk>/delete", CourseDeleteView.as_view(), name="course-delete"),
    path("about/", about, name="courses-about"),
    path(
        "<slug:course_id>/lessons/",
        lesson_detail_view,
        name="lesson-detail",
    ),
    path(
        "<slug:course_id>/video/<slug:video_id>/",
        lesson_video_view,
        name="lesson-video-detail",
    ),
    path("watchtime/create/", watchtime_create, name="watchtime-create"),
    path(
        "get-certificate/<slug:course_id>/",
        generate_certificate_view,
        name="certificate",
    ),
]