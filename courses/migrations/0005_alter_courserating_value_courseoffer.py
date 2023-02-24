# Generated by Django 4.1.2 on 2023-02-09 18:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_remove_course_last_video_watched"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courserating",
            name="value",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "poor"),
                    (2, "fair"),
                    (3, "good"),
                    (4, "very good"),
                    (5, "excellent"),
                ],
                default=0,
                help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
                verbose_name="rating value",
            ),
        ),
        migrations.CreateModel(
            name="CourseOffer",
            fields=[
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("pkid", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "discounted_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_offer",
                        to="courses.course",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]
