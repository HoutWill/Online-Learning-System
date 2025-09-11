from django.shortcuts import render, redirect , get_object_or_404   
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from courses.models import Course , Category , CourseReview
from enrollment.models import Enrollment
from accounts.models import User
from django.http import HttpResponseForbidden
from accounts.forms import UserRegistrationForm  # reuse your registration form
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Avg, Count
from django.db import models




User = get_user_model()
@login_required
def profile_view(request):
    return render(request, "profile.html", {"user": request.user})
def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'instructor':
            return redirect('instructor_dashboard')
        elif request.user.role == 'employee':
            return redirect('employee_dashboard')
        # Unknown role → log out or forbid
        logout(request)
        return redirect('login_view')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'instructor':
                return redirect('instructor_dashboard')
            elif user.role == 'employee':
                return redirect('employee_dashboard')
            logout(request)
            return redirect('login_view')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



@login_required
@role_required("student")
def student_dashboard(request):
    categories = Category.objects.all()
    all_courses = Course.objects.all()

    # Search functionality
    query = request.GET.get('q')
    if query:
        all_courses = all_courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(instructor__username__icontains=query)
        )

    courses_with_progress = []
    for course in all_courses:
        # Enrollment progress
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            progress = enrollment.progress
            completed = enrollment.completed
        except Enrollment.DoesNotExist:
            progress = 0
            completed = False

        # Ratings including all students
        rating_data = course.reviews.aggregate(
            avg_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        avg_rating = round(rating_data['avg_rating'] or 0)  # round to nearest integer
        total_reviews = rating_data['total_reviews']

        # Current student's rating (for highlighting)
        user_review = CourseReview.objects.filter(course=course, student=request.user).first()
        user_rating = int(user_review.rating) if user_review else 0  # 0 if not rated

        courses_with_progress.append({
            'course': course,
            'progress': progress,
            'completed': completed,
            'avg_rating': avg_rating,        # overall average (integer)
            'total_reviews': total_reviews,
            'user_rating': user_rating       # current student's rating
        })

    context = {
        'categories': categories,
        'courses_with_progress': courses_with_progress,
        'query': query
    }
    return render(request, "student_dashboard.html", context)


@login_required
@role_required("instructor", "employee")
def instructor_dashboard(request):
    all_courses = Course.objects.all()        # All courses for "All Courses" tab
    categories = Category.objects.all()       # All categories to build tabs

    context = {
        'all_courses': all_courses,
        'categories': categories
    }
    return render(request, 'instructor_dashboard.html', context)



@login_required
@role_required("employee")
def employee_dashboard(request):
    # Stats
    total_users = User.objects.count()
    total_students = User.objects.filter(role="student").count()
    total_instructors = User.objects.filter(role="instructor").count()
    total_employees = User.objects.filter(role="employee").count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()

    # Data for management tabs (reuse cards like instructor dashboard)
    users = User.objects.all()
    courses = Course.objects.all()
    enrollments = Enrollment.objects.select_related("student", "course")

    context = {
        "total_users": total_users,
        "total_students": total_students,
        "total_instructors": total_instructors,
        "total_employees": total_employees,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "users": users,
        "courses": courses,
        "enrollments": enrollments,
    }

    return render(request, "employee_dashboard.html", context)

    
def logout_view(request):
    """
    Handles user logout and redirects to the login page.
    """
    logout(request)
    return redirect('login_view')
@login_required
def profile_view(request):
    return render(request, "profile.html")




@login_required
@role_required("employee")
def user_list(request):
    users = User.objects.all()
    return render(request, "employee/user_list.html", {"users": users})

@login_required
@role_required("employee")
def user_add(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserRegistrationForm()
    return render(request, "employee/user_add.html", {"form": form})

@login_required
@role_required("employee")
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("user_list")
    return render(request, "employee/user_delete.html", {"user": user})
@login_required
@role_required("employee")
def course_list_employee(request):
    courses = Course.objects.all()
    return render(request, "employee/course_list.html", {"courses": courses})

@login_required
@role_required("employee")
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    return render(request, "employee/enrollment_list.html", {"enrollments": enrollments})