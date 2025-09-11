import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
from courses.models import Category, Course, CourseReview
from lessons.models import Lesson, LessonContent
from accounts.models import User
from enrollment.models import Enrollment

class Command(BaseCommand):
    help = "Create 3 software development courses with lessons, reviews, and generated images"

    def handle(self, *args, **kwargs):
        # Folder to save images
        image_dir = os.path.join("media", "courses", "image")
        os.makedirs(image_dir, exist_ok=True)

        # Function to generate unique course image
        def generate_course_image(course_title):
            bg_color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
            img = Image.new("RGB", (600, 400), color=bg_color)
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", 30)
            except:
                font = ImageFont.load_default()

            # Wrap text
            lines = []
            words = course_title.split()
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                bbox = draw.textbbox((0,0), test_line, font=font)
                w = bbox[2] - bbox[0]
                if w > 550:
                    lines.append(line)
                    line = word
                else:
                    line = test_line
            lines.append(line)

            y = 150
            for l in lines:
                bbox = draw.textbbox((0,0), l, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                draw.text(((600 - w) / 2, y), l, fill=(0,0,0), font=font)
                y += h + 5

            img_path = os.path.join(image_dir, f"{course_title.replace(' ', '_')}.png")
            img.save(img_path)
            return img_path

        # Instructor
        instructor = User.objects.filter(is_staff=True).first()
        if not instructor:
            self.stdout.write(self.style.ERROR("No instructor found! Create at least one staff user."))
            return

        students = User.objects.filter(is_staff=False)
        if not students.exists():
            self.stdout.write(self.style.ERROR("No student users found! Create some student accounts."))
            return

        # Category
        category, _ = Category.objects.get_or_create(name="Software Development")

        # Delete old courses in this category
        old_courses = Course.objects.filter(category=category)
        old_courses.delete()
        self.stdout.write(self.style.WARNING("Deleted old courses in Software Development category."))

        # Example 3 courses
        courses_data = [
            {"title": "Python Programming", "description": "Learn Python from scratch."},
            {"title": "Django Web Development", "description": "Build web apps with Django."},
            {"title": "React for Beginners", "description": "Build frontend apps using React."},
        ]

        for course_info in courses_data:
            course = Course.objects.create(
                category=category,
                title=course_info["title"],
                description=course_info["description"],
                price=round(random.randint(20, 100), 2),
                instructor=instructor,
                published_status=True
            )

            # Generate and save image
            img_path = generate_course_image(course_info["title"])
            with open(img_path, "rb") as f:
                course.image.save(f"{course_info['title'].replace(' ', '_')}.png", File(f), save=True)

            self.stdout.write(self.style.SUCCESS(f"Created course: {course.title}"))

            # Add 3 lessons
            for idx in range(1, 4):
                lesson_title = f"Lesson {idx} - {course.title}"
                lesson = Lesson.objects.create(
                    course=course,
                    title=lesson_title,
                    order=idx,
                    published=True
                )
                LessonContent.objects.create(
                    lesson=lesson,
                    description=f"Content for {lesson_title}",
                    video_url="",
                    document=""
                )
                self.stdout.write(self.style.SUCCESS(f"  Added lesson: {lesson.title}"))

            # Add reviews and progress for students
            for student in students:
                rating = random.randint(1, 5)
                comment = f"Auto review ({rating} stars) by {student.username}"
                CourseReview.objects.update_or_create(
                    course=course,
                    student=student,
                    defaults={"rating": rating, "comment": comment}
                )

                progress = random.randint(0, 100)
                completed = progress == 100
                Enrollment.objects.update_or_create(
                    student=student,
                    course=course,
                    defaults={"progress": progress, "completed": completed}
                )

            self.stdout.write(self.style.SUCCESS(f"  Added reviews and progress for {students.count()} students"))

        self.stdout.write(self.style.SUCCESS("All 3 courses created successfully with unique images!"))
