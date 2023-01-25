from celery import shared_task

from django.db import transaction
from django.http import HttpResponse
from .models import Course, Lesson, Video
from .utils import (
    yt_playlist_details,
    yt_playlist_videos,
    yt_video_duration,
    youtube_duration_convertion,
)


@shared_task
def create_course_from_ytplaylist():
    pass


@shared_task(bind=True)  # shared task must always be first
@transaction.atomic
def yt_playlist_create_course(user, playlist_id):
    """
    function for creating course from a youtube playlist url
    """
    playlist_details = yt_playlist_details(playlist_id)
    video_list = yt_playlist_videos(playlist_id)
    print(playlist_details)
    try:
        course = Course.objects.create(
            author=user,
            title=playlist_details["title"],
            playlist=playlist_id,
            brief_description=playlist_details["description"],
            thumbnail_url=playlist_details["thumbnails"]["standard"]["url"],
            # youtube_channel=playlist_details["channelTitle"],
        )
        try:
            lesson = Lesson.objects.create(
                course=course,
                title="Lesson 1",
                position=1,
            )
            try:
                total_lesson_time = 0
                for video in video_list:
                    video_id = video["video_id"]
                    yt_duration = yt_video_duration(video_id)
                    video_seconds, cleaned_total_time = youtube_duration_convertion(
                        yt_duration
                    )
                    Video.objects.create(
                        lesson=lesson,
                        course=course,
                        title=video["title"],
                        position=video["position"],
                        video_id=video_id,
                        duration_seconds=video_seconds,
                        duration_time=cleaned_total_time,
                    )
                    total_lesson_time += video_seconds

                lesson.total_video_seconds = total_lesson_time
                course.total_watch_time = total_lesson_time
                lesson.save()
                course.save()
                print("i am finished working")
                return course
            except:
                return HttpResponse("Sorry o video fault")

        except Exception as e:
            print(e)
            print("Sorry o lesson fault")
            return HttpResponse("Sorry o lesson fault")

    except Exception as e:
        print(e)

        return HttpResponse(e)
