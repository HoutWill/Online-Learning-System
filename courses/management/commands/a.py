from django.core.management.base import BaseCommand
from lessons.models import Lesson, LessonContent
from courses.models import Course
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Create IT Support and Photoshop beginner courses with 2 lessons each"

    def handle(self, *args, **kwargs):
        # Delete old courses if exist
        Course.objects.filter(title__in=["IT Support Basics", "Photoshop Basics"]).delete()
        self.stdout.write(self.style.WARNING("Deleted old courses if existed."))

        # IT Support Basics course
        it_course = Course.objects.create(
            title="IT Support Basics",
            description="Learn the fundamentals of IT support including troubleshooting, hardware, and software maintenance.",
            price=49.99,
            instructor_id=1,  # Replace with your instructor user ID
            category_id=2,    # Replace with IT Support category ID
            published_status=True
        )

        it_lessons = [
            ("Introduction to IT Support", "", 
             "Understand what IT support professionals do, key roles, and how to approach troubleshooting basic issues."),
            ("Basic Troubleshooting", "https://www.youtube.com/embed/2ePf9rue1Ao", 
             "Learn step-by-step troubleshooting for software and hardware issues. Real-world examples: fixing slow computers, printer errors.")
        ]

        for idx, (title, video_url, description) in enumerate(it_lessons, start=1):
            lesson = Lesson.objects.create(
                course=it_course,
                title=f"Lesson {idx} - {title}",
                order=idx,
                published=True
            )
            LessonContent.objects.create(
                lesson=lesson,
                description=description,
                video_url=video_url,
                document=""
            )

        self.stdout.write(self.style.SUCCESS("Created IT Support course with 2 lessons."))

        # Photoshop Basics course
        ps_course = Course.objects.create(
            title="Photoshop Basics",
            description="Learn Adobe Photoshop from scratch. Create stunning graphics and edit images like a pro.",
            price=59.99,
            instructor_id=1,  # Replace with your instructor user ID
            category_id=3,    # Replace with Photoshop category ID
            published_status=True
        )

        ps_lessons = [
            ("Introduction to Photoshop", "", 
             "Learn the Photoshop interface, tools, and basic functions. Example: opening files, understanding layers."),
            ("Basic Image Editing", "https://www.youtube.com/embed/5dKY1bP66Fo", 
             "Apply basic edits like crop, resize, adjust brightness/contrast, and use selection tools.")
        ]

        for idx, (title, video_url, description) in enumerate(ps_lessons, start=1):
            lesson = Lesson.objects.create(
                course=ps_course,
                title=f"Lesson {idx} - {title}",
                order=idx,
                published=True
            )
            LessonContent.objects.create(
                lesson=lesson,
                description=description,
                video_url=video_url,
                document=""
            )

        self.stdout.write(self.style.SUCCESS("Created Photoshop course with 2 lessons."))
        self.stdout.write(self.style.SUCCESS("✅ IT Support and Photoshop courses setup completed!"))
