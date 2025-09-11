from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CourseForm , CourseReviewForm
from .models import Course, Category , CourseReview
from accounts.decorators import role_required

# ------------------------
# Helper: redirect by role
# ------------------------
def redirect_by_role(user):
    """
    Redirect user based on their role.
    """
    if user.role == "instructor":
        return redirect("instructor_dashboard")
    elif user.role == "employee":
        return redirect("employee_dashboard")
    elif user.role == "student":
        return redirect("student_dashboard")
    else:
        return redirect("/")


# =========================
# Course Add / Edit
# =========================
@login_required
@role_required("instructor", "employee")
def course_add_edit(request, pk=None):
    if pk:
        # Edit existing course
        course = get_object_or_404(Course, pk=pk)
    else:
        # Add new course
        course = None

    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if form.is_valid():
        new_course = form.save(commit=False)
        if request.user.role == "instructor":
            new_course.instructor = request.user
        new_course.save()
        return redirect_by_role(request.user)  # Dynamic redirect

    return render(
        request,
        "course_add.html",
        {
            "form": form,
            "course": course,
            "cancel_url": redirect_by_role(request.user).url,
        },
    )


# =========================
# Course Delete
# =========================
@login_required
@role_required("instructor", "employee")
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect_by_role(request.user)  # Dynamic redirect
    
    return render(
        request,
        "course_delete.html",
        {
            "course": course,
            "cancel_url": redirect_by_role(request.user).url,
        },
    )


# =========================
# Category Add
# =========================
@login_required
@role_required("instructor", "employee")
def category_add(request):
    error = None
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            if Category.objects.filter(name=name).exists():
                error = "Category with this name already exists."
            else:
                Category.objects.create(name=name)
                return redirect_by_role(request.user)  # Dynamic redirect
        else:
            error = "Please provide a category name."

    return render(
        request,
        "category_add.html",
        {
            "error": error,
            "cancel_url": redirect_by_role(request.user).url,
        },
    )   

@login_required
def course_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Get the current user's review if exists
    try:
        existing_review = CourseReview.objects.get(course=course, student=request.user)
    except CourseReview.DoesNotExist:
        existing_review = None

    if request.method == "POST":
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment", "").strip()

        if existing_review:
            # Update the existing review
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
        else:
            # Create a new review
            CourseReview.objects.create(
                course=course,
                student=request.user,
                rating=rating,
                comment=comment
            )

        # Redirect to student dashboard instead of course review page
        return redirect("student_dashboard")  

    # Fetch all reviews for display
    reviews = course.reviews.select_related("student").all()

    context = {
        "course": course,
        "existing_review": existing_review,
        "reviews": reviews
    }
    return render(request, "course_review.html", context)


# =========================
# Category Edit
# =========================
@login_required
@role_required("instructor", "employee")
def category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    error = None

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            if Category.objects.filter(name=name).exclude(pk=category_id).exists():
                error = "Category with this name already exists."
            else:
                category.name = name
                category.save()
                return redirect_by_role(request.user)
        else:
            error = "Please provide a category name."

    return render(
        request,
        "category_edit.html",
        {
            "category": category,
            "error": error,
            "cancel_url": redirect_by_role(request.user).url,
        },
    )


# =========================
# Category Delete
# =========================
@login_required
@role_required("instructor", "employee")
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        category.delete()
        return redirect_by_role(request.user)

    return render(
        request,
        "category_delete.html",
        {
            "category": category,
            "cancel_url": redirect_by_role(request.user).url,
        },
    )
