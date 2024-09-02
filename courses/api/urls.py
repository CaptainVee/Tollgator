from django.urls import path
from courses.api.views import (
    TopEnrolledCoursesView,
    CourseDetailAPIView,
    CoursesByCategoryAPIView,
    CategoryCreateListView,
    CourseSearchView,
    AutocompleteView,
)


urlpatterns = [
    path("api/v1/courses/", TopEnrolledCoursesView.as_view(), name="api-courses-list"),
    path(
        "api/v1/courses/<slug:slug>/",
        CourseDetailAPIView.as_view(),
        name="api-course-detail",
    ),
    path(
        "api/v1/categories/<uuid:category_id>/courses/",
        CoursesByCategoryAPIView.as_view(),
        name="api-category-courses",
    ),
    path(
        "api/v1/categories/",
        CategoryCreateListView.as_view(),
        name="api-categories-list",
    ),
    path(
        "api/v1/search/courses/", CourseSearchView.as_view(), name="api-courses-search"
    ),
    path(
        "api/v1/search/autocomplete/",
        AutocompleteView.as_view(),
        name="api-courses-autocomplete",
    ),
]
