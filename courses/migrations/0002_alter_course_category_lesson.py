# Generated by Django 4.1.2 on 2022-10-29 19:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[("S", "Shirt"), ("SW", "Sport wear"), ("OW", "Outwear")],
                max_length=2,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=120)),
                ("video_url", models.URLField(blank=True, max_length=300)),
                ("position", models.IntegerField()),
                (
                    "description",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="courses.course"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]
