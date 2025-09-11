# enrollments/models.py
from django.db import models
from django.conf import settings
from courses.models import Course
from lessons.models import Lesson
from django.utils import timezone

# -------------------------------
# Enrollment Model
# -------------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


# -------------------------------
# Lesson Progress Model
# -------------------------------
class LessonProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"{self.student.username} - {self.lesson.title} ({status})"


# -------------------------------
# Signal to auto-update Enrollment progress
# -------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=LessonProgress)
def update_enrollment_progress(sender, instance, **kwargs):
    course = instance.lesson.course
    student = instance.student
    total_lessons = course.lesson_set.count()
    if total_lessons == 0:
        return

    completed_lessons = LessonProgress.objects.filter(
        student=student,
        lesson__course=course,
        completed=True
    ).count()

    enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
    enrollment.progress = (completed_lessons / total_lessons) * 100
    enrollment.completed = enrollment.progress == 100
    enrollment.save()
