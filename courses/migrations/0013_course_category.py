# Generated by Django 4.1.2 on 2024-05-02 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0012_course_tags_alter_course_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="courses.category",
            ),
        ),
    ]
