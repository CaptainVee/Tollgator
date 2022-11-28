from django.urls import path
from . import views
from .views import (
    CourseListView,
    user_course_list_view,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    lesson_create_view,
    lesson_update_view,
    lesson_list_view,
    lesson_video,
    get_video_url,
    lesson_detail_view,
    enroll,
    clear_messages,
    video_update_view,
    new,
)

# from .views import  add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView, , StartDetailView

# app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="courses-home"),
    path("new/", new, name="new"),
    path("user/", user_course_list_view, name="user-course-list"),
    path("course/new/", CourseCreateView.as_view(), name="course-create"),
    path(
        "course/<slug:course_slug>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
    path("course/<int:pk>/update/", CourseUpdateView.as_view(), name="course-update"),
    path("course/<int:pk>/delete", CourseDeleteView.as_view(), name="course-delete"),
    # path("about/", views.about, name="courses-about"),
    path(
        "course/<slug:course_slug>/lessons/",
        lesson_list_view,
        name="lesson-list",
    ),
    path("lesson/<slug:course_id>/new/", lesson_create_view, name="lesson-create"),
    path(
        "<slug:course_id>/lesson/<slug:lesson_id>/",
        lesson_detail_view,
        name="lesson-detail",
    ),
    path(
        "<slug:course_slug>/lesson/<slug:lesson_slug>/<slug:video_slug>/",
        lesson_video,
        name="lesson-video-detail",
    ),
    path(
        "course/<slug:course_slug>/enroll/",
        enroll,
        name="enroll",
    ),
]


htmx_urlpatterns = [
    path(
        "video/update/<slug:lesson_id>/<slug:video_id>/",
        video_update_view,
        name="video-update",
    ),
    path(
        "video/new/<slug:lesson_id>/",
        video_update_view,
        name="video-create",
    ),
    path(
        "<slug:course_id>/lesson_update/<slug:lesson_id>/",
        lesson_update_view,
        name="lesson-update",
    ),
    path("video/<slug:video_slug>", get_video_url, name="video-url"),
    path("clear/", clear_messages, name="clear"),
]

urlpatterns += htmx_urlpatterns
