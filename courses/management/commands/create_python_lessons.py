from django.core.management.base import BaseCommand
from lessons.models import Lesson, LessonContent, Assignment
from courses.models import Course
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Create Django for Beginners course with lessons and assignment"

    def handle(self, *args, **kwargs):
        # Get Django course
        django_course, created = Course.objects.get_or_create(
            title="Django for Beginners",
            defaults={
                "category_id": 1,  # Replace with your actual Software Development category ID
                "description": "Learn Django from scratch, covering models, views, templates, and basic web apps.",
                "price": 49.99,
                "instructor_id": 1,  # Replace with your instructor user ID
                "published_status": True,
            }
        )

        # Delete old lessons & assignments
        django_course.lesson_set.all().delete()
        django_course.assignments.all().delete()

        # Lessons data
        lessons_data = [
            (
                "Lesson 1 - Django Introduction & Setup",
                "https://www.youtube.com/watch?v=F5mRW0jo-U4",
                "Introduction to Django, installation, and project setup. Learn about virtual environments, Django apps, and running the development server."
            ),
            (
                "Lesson 2 - Models and Migrations",
                "https://www.youtube.com/watch?v=UmljXZIypDc",
                "Learn how to define models, fields, and relationships. Understand migrations and how to apply them to update your database."
            ),
            (
                "Lesson 3 - Views & URLs",
                "https://www.youtube.com/watch?v=F5mRW0jo-U4",
                "Learn how to write views to handle requests and responses. Understand URL routing and how to connect URLs to views."
            ),
            (
                "Lesson 4 - Templates & Static Files",
                "https://www.youtube.com/watch?v=V0Sg3U4a7v0",
                "Create dynamic HTML pages using Django templates. Learn about template inheritance, context data, and serving static files."
            ),
            (
                "Lesson 5 - Forms & User Input",
                "https://www.youtube.com/watch?v=H5v5T7wXJc8",
                "Learn how to handle forms in Django. Validate user input, create model forms, and process form submissions securely."
            ),
            (
                "Lesson 6 - Admin Interface & Deployment",
                "https://www.youtube.com/watch?v=3Y1NJmsJpE0",
                "Explore the Django admin interface, customize it, and prepare your project for deployment. Learn about basic security and hosting options."
            ),
        ]

        # Create lessons and content
        for idx, (title, video_url, description) in enumerate(lessons_data, start=1):
            lesson = Lesson.objects.create(
                course=django_course,
                title=title,
                order=idx,
                published=True
            )
            LessonContent.objects.create(
                lesson=lesson,
                description=description,
                video_url=video_url,
                document=""  # You can set a file path if you want
            )

        # Create one assignment
        Assignment.objects.create(
            course=django_course,
            title="Build a Simple Blog App",
            description=(
                "Using the concepts from the lessons, create a simple blog application. "
                "Implement models for posts, views for listing and detail pages, templates for rendering content, "
                "and the admin interface for managing posts. Optional: Add basic user authentication."
            ),
            due_date=datetime.now() + timedelta(days=7)
        )

        self.stdout.write(self.style.SUCCESS("✅ Django for Beginners lessons and assignment created successfully!"))
