# Generated by Django 4.1.2 on 2022-12-14 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0023_alter_video_duration_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="duration_time",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
