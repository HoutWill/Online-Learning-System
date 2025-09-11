from django.shortcuts import get_object_or_404, redirect , render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Enrollment, LessonProgress
from lessons.models import Lesson
from courses.models import Course
from django.contrib import messages
from accounts.models import User
# -------------------------------
# Browse all courses
# -------------------------------
@login_required
@role_required('student')
def browse_courses(request):
    courses = Course.objects.exclude(enrollment__student=request.user)

    return render(request, "enrollments/browse_courses.html", {"courses": courses})

# -------------------------------
# Enroll in a course
# -------------------------------
@login_required
@role_required('student')
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f"You have enrolled in {course.title}!")
    else:
        messages.info(request, f"You are already enrolled in {course.title}.")
    # Redirect directly to lesson list of this course
    return redirect("lesson_list", course_id=course.id)

# -------------------------------
# Redirect student to lesson list of first enrolled course
# -------------------------------
@login_required
@role_required('student')
def my_courses(request):
    enrollment = Enrollment.objects.filter(student=request.user).select_related('course').first()
    if enrollment:
        # Redirect to lesson list of the first enrolled course
        return redirect("lesson_list", course_id=enrollment.course.id)
    else:
        # If no courses enrolled, redirect to browse
        return redirect("browse_courses")

# -------------------------------
# Mark a lesson as completed
# -------------------------------
@login_required
@role_required('student')
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    progress, _ = LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
    if not progress.completed:
        progress.completed = True
        progress.save()
        messages.success(request, f"Lesson '{lesson.title}' marked as completed!")
    return redirect("lesson_list", course_id=lesson.course.id)

@login_required
@role_required('employee')
def manage_enrollments(request):
    enrollments = Enrollment.objects.select_related("student", "course").all()
    return render(request, "manage_enrollments.html", {"enrollments": enrollments})
# -------------------------------
# Manually enroll a student (form-based)
# -------------------------------
@login_required
@role_required('employee')
def add_enrollment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = User.objects.filter(role="student")  # all students

    if request.method == "POST":
        student_id = request.POST.get("student")
        student = get_object_or_404(User, pk=student_id, role="student")
        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            messages.success(request, f"{student.username} enrolled in {course.title}.")
        else:
            messages.info(request, f"{student.username} is already enrolled in {course.title}.")
        return redirect("course_enrollments", course_id=course.id)

    return render(request, "add_enrollment.html", {"course": course, "students": students})



# -------------------------------
# Remove enrollment
# -------------------------------
@login_required
@role_required('employee')
def remove_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    course_id = enrollment.course.id
    enrollment.delete()
    messages.success(request, f"Enrollment removed successfully.")
    return redirect("course_enrollments", course_id=course_id)

@login_required
@role_required('employee')
def course_enrollments(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related("student")
    return render(request, "course_enrollments.html", {"course": course, "enrollments": enrollments})