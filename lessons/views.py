from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from courses.models import Course
from .models import Lesson, LessonContent , Assignment , Submission 
from .forms import LessonForm, LessonContentForm , AssignmentForm , SubmissionForm
from enrollment.models import LessonProgress
# ------------------------
# Helper for role-based redirect
# ------------------------
def redirect_by_role(user, course_id=None):
    """
    Redirect users after actions based on their role.
    """
    if user.role == "instructor":
        return redirect("lesson_list", course_id=course_id)
    elif user.role == "student":
        return redirect("lesson_list", course_id=course_id)
    elif user.role == "employee":
        return redirect("lesson_list", course_id=course_id)
    else:
        return redirect("/")

# ------------------------
# LESSON VIEWS
# ------------------------

# Show all lessons of a course
# lesson_list view (student progress)


@login_required
@role_required("instructor", "student", "employee")
def lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)

    # Ensure every lesson has a content object
    for lesson in lessons:
        content, _ = LessonContent.objects.get_or_create(lesson=lesson)
        lesson.content = content  # attach dynamically

    user_role = request.user.role

    completed_ids = []
    if user_role == "student":
        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__course=course,
            completed=True
        )
        completed_ids = completed_lessons.values_list("lesson_id", flat=True)

    # Fetch assignments for this course
    assignments = Assignment.objects.filter(course=course)

    # For students: attach submission if exists
    if user_role == "student":
        for a in assignments:
            submission = Submission.objects.filter(student=request.user, assignment=a).first()
            a.submission = submission

    context = {
        "course": course,
        "lessons": lessons,
        "user_role": user_role,
        "completed_ids": completed_ids,
        "assignments": assignments
    }
    return render(request, "lesson_list.html", context)
# Add or edit a lesson
@login_required
@role_required("instructor")
def lesson_add_edit(request, course_id=None, lesson_id=None):
    if lesson_id:
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        course = lesson.course
    else:
        lesson = None
        course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.course = course
            new_lesson.save()
            return redirect_by_role(request.user, course_id=course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, "lesson_add.html", {"form": form, "course": course})

# Add/Edit lesson content
@login_required
@role_required("instructor")
def lesson_content_edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    content, _ = LessonContent.objects.get_or_create(lesson=lesson)

    if request.method == "POST":
        form = LessonContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect_by_role(request.user, course_id=lesson.course.id)
    else:
        form = LessonContentForm(instance=content)

    return render(request, "lesson_content_edit.html", {
        "form": form,
        "lesson": lesson
    })

# Show lesson detail with content (instructor only)
@login_required
@role_required("instructor")
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    content, _ = LessonContent.objects.get_or_create(lesson=lesson)

    return render(request, "lesson_detail.html", {
        "lesson": lesson,
        "content": content
    })

# Delete a lesson
@login_required
@role_required("instructor")
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course_id = lesson.course.id

    if request.method == "POST":
        lesson.delete()
        return redirect_by_role(request.user, course_id=course_id)

    return render(request, "lesson_delete.html", {
        "lesson": lesson,
        "course": lesson.course
    })
@login_required
@role_required("instructor")
def assignment_list(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    assignments = Assignment.objects.filter(course=course)
    return render(request, "assignments/assignment_list.html", {
        "course": course,
        "assignments": assignments
    })


# Create or edit an assignment
# Create or edit an assignment
@login_required
@role_required("instructor")
def assignment_add_edit(request, course_id=None, assignment_id=None):
    if assignment_id:
        assignment = get_object_or_404(Assignment, pk=assignment_id, course__instructor=request.user)
        course = assignment.course
    else:
        assignment = None
        course = get_object_or_404(Course, id=course_id, instructor=request.user)

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.course = course
            new_assignment.save()
            # Redirect using role-based helper
            return redirect_by_role(request.user, course_id=course.id)
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, "assignments/assignment_form.html", {
        "form": form, 
        "course": course,
        "back_url": redirect_by_role(request.user, course_id=course.id)  # pass back url
    })


# Delete assignment
@login_required
@role_required("instructor")
def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id, course__instructor=request.user)
    course_id = assignment.course.id

    if request.method == "POST":
        assignment.delete()
        return redirect_by_role(request.user, course_id=course_id)

    return render(request, "assignments/assignment_confirm_delete.html", {
        "assignment": assignment,
        "back_url": redirect_by_role(request.user, course_id=course_id)
    })


@login_required
@role_required("student")
def submission_add(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.assignment = assignment
            sub.student = request.user
            sub.save()
            # Redirect to lesson_list after submission
            return redirect("lesson_list", course_id=assignment.course.id)
    else:
        form = SubmissionForm()
    
    return render(request, "assignments/submission_form.html", {
        "form": form,
        "assignment": assignment,
        "back_url": redirect_by_role(request.user, course_id=assignment.course.id)
    })
