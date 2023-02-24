# Generated by Django 4.1.2 on 2022-12-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_delete_certificate"),
        ("user", "0002_enrollment_course_userdashboard_courses_enrolled"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userdashboard",
            name="courses_enrolled",
        ),
        migrations.AddField(
            model_name="userdashboard",
            name="courses",
            field=models.ManyToManyField(
                blank=True,
                related_name="courses",
                through="user.Enrollment",
                to="courses.course",
            ),
        ),
    ]
