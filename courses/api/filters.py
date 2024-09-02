import django_filters as filters
from courses.models import Course


class CourseFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    brief_description = filters.CharFilter(
        field_name="brief_description", lookup_expr="icontains"
    )
    content = filters.CharFilter(field_name="content", lookup_expr="icontains")
    tags = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")
    category = filters.CharFilter(field_name="category__name", lookup_expr="iexact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Course
        fields = [
            "author",
            "title",
            "tags",
            "brief_description",
            "content",
            "category__name",
            "created_at",
            "updated_at",
        ]
