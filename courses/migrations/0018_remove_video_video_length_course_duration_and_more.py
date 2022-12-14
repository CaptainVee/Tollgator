# Generated by Django 4.1.2 on 2022-12-13 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0017_course_thumbnail_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="video",
            name="video_length",
        ),
        migrations.AddField(
            model_name="course",
            name="duration",
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="video",
            name="video_duration",
            field=models.DurationField(blank=True, null=True),
        ),
    ]
