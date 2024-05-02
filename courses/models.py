from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.db.models import Avg, Sum
from django_quill.fields import QuillField

# from django_countries.fields import CountryField
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from common.utils import convert_currency_to_local
from common.models import BaseModel, Currency
from common.constants import RATING


User = settings.AUTH_USER_MODEL


class Course(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=150, unique=True)
    brief_description = models.CharField(max_length=500, blank=True, null=True)
    content = QuillField(blank=True, null=True)
    slug = AutoSlugField(populate_from="title", always_update=False, unique=True)
    tags = ArrayField(
        models.CharField(max_length=200, default="", blank=True),
        blank=True,
        default=list,
    )
    thumbnail = models.ImageField(default="default.jpg", null=True, blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    total_watch_time = models.PositiveIntegerField(null=True, default=0)
    # youtube_channel = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=False
    )
    translation = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)
    is_private = models.BooleanField(
        default=True, help_text="uncheck this box for your course to go public"
    )

    def clean(self):
        if self.price < 0:
            raise ValidationError({"price": _("price must be positive.")})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def lessons(self):
        return self.lesson_set.all().order_by("position")

    @property
    def video_count(self):
        return self.video_set.all().count()

    def last_video_watched(self, user):
        enrollment = self.enrollment_set.get(user_dashboard__user=user)
        if enrollment.last_video_watched is None:
            enrollment.last_video_watched = self.video_set.last()
            enrollment.save()
        return enrollment.last_video_watched

    @property
    def get_price(self):
        course_offer = self.get_discounted_price()
        if course_offer:
            return course_offer.discounted_price
        else:
            return self.price

    def get_local_price(self, user):
        return convert_currency_to_local(user.currency, self.currency, self.get_price)

    def get_discounted_price(self):
        return self.course_offer.filter(discounted_price__isnull=False).first()

    def get_percentage_off(self):
        course_offer = self.get_discounted_price()
        percentage_off = round((course_offer.discounted_price / self.price) * 100)
        return f"{percentage_off}% Off"

    def get_absolute_url(self):
        return reverse("course-update", kwargs={"pk": self.pk})

    def get_average_rating(self):
        """gives the average number of reviews a course has. eg (4.5) stars"""
        average = self.course_rating.aggregate(Avg("value"))["value__avg"]
        return 0 if average is None else average

    def get_rating_count(self):
        """gives the number of reviews a course has. eg (50) reviews"""
        return self.course_rating.all().count()

    def get_enrollment_count(self):
        """gives the number of student that has enrolled for a course"""
        return self.enrollment_set.all().count()

    def get_total_revenue(self):
        revenue = self.course_order.filter(ordered=True).aggregate(
            Sum("course__price")
        )["course__price__sum"]
        return 0 if revenue is None else revenue

    # def get_add_to_cart_url(self):
    #     return reverse("add-to-cart", kwargs={"pk": self.pk})

    # def get_remove_from_cart_url(self):
    #     return reverse("remove-from-cart", kwargs={"pk": self.pk})


class Lesson(BaseModel):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=250, null=True, blank=True)
    total_video_seconds = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title

    def get_course(self):
        return self.course.title

    def get_absolute_url(self):
        return reverse(
            "lesson-detail",
            kwargs={"course_slug": self.course.slug, "lesson_id": self.id},
        )

    @property
    def videos(self):
        return self.video_set.all().order_by("position")


class Video(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    video_id = models.CharField(max_length=15, null=False, blank=False)
    video_url = models.URLField(max_length=300, blank=True, null=True)
    position = models.PositiveSmallIntegerField()
    duration_seconds = models.PositiveIntegerField(null=True, default=0)
    duration_time = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "lesson-video-detail",
            kwargs={
                "course_id": self.lesson.course.id,
                "video_id": self.id,
            },
        )


class WatchTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    finished_video = models.BooleanField(default=False)
    stopped_at = models.PositiveIntegerField(blank=True, null=True, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def start(self):
        if self.stopped_at < 10:
            return self.stopped_at
        return self.stopped_at - 5

    def __str__(self):
        return f"watch time for {self.video}"


class CourseRating(BaseModel):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="course_rating",
    )
    rated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="user_who_rated",
    )
    value = models.PositiveSmallIntegerField(
        verbose_name=_("rating value"),
        choices=RATING,
        default=0,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
    )
    review = models.TextField()

    def __str__(self):
        return f"{self.rated_by}"


class CourseOffer(BaseModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="course_offer",
    )
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.discounted_price < 0:
            raise ValidationError(
                {"discounted_price": _("Discounted price must be positive.")}
            )
        if self.discounted_price > self.course.price:
            raise ValidationError(
                {
                    "discounted_price": _(
                        "Discounted price cannot be higher than the regular price."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Category(BaseModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
