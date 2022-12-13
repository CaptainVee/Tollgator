from django.urls import path
from . import views
from .views import (
    Home,
    CourseListView,
    UserCourseListView,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    course_create_playlist_view,
    lesson_detail_view,
    lesson_create_update,
    lesson_video_view,
    video_create_update,
    get_video_url,
    enroll,
    clear_messages,
    get_spinner,
    generate_certificate_view,
    new,
)

# from .views import  add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView, , StartDetailView

# app_name = "courses"

urlpatterns = [
    path("", Home.as_view(), name="course-home"),
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("new/", new, name="new"),
    path("instructor/dashboard", UserCourseListView.as_view(), name="user-course-list"),
    path("course/new/", CourseCreateView.as_view(), name="course-create"),
    path(
        "course/new/playlist",
        course_create_playlist_view,
        name="course-create-playlist",
    ),
    path(
        "course/<slug:course_slug>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
    path("course/<int:pk>/update/", CourseUpdateView.as_view(), name="course-update"),
    path("course/<int:pk>/delete", CourseDeleteView.as_view(), name="course-delete"),
    # path("about/", views.about, name="courses-about"),
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
    path(
        "course/<slug:course_slug>/enroll/",
        enroll,
        name="enroll",
    ),
    path(
        "get-certificate/<slug:course_id>/",
        generate_certificate_view,
        name="certificate",
    ),
]


htmx_urlpatterns = [
    path(
        "<slug:course_id>/lesson/<slug:lesson_id>/",
        lesson_create_update,
        name="lesson-detail",
    ),
    path(
        "<slug:course_id>/lesson/new/",
        lesson_create_update,
        name="lesson-new",
    ),
    path(
        "video/update/<slug:lesson_id>/<slug:video_id>/",
        video_create_update,
        name="video-update",
    ),
    path(
        "video/new/<slug:lesson_id>/",
        video_create_update,
        name="video-create",
    ),
    path("video/<slug:video_slug>", get_video_url, name="video-url"),
    path("spinner/", get_spinner, name="get-spinner"),
    path("clear/", clear_messages, name="clear"),
]

urlpatterns += htmx_urlpatterns
