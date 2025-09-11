# enrollments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.browse_courses, name="browse_courses"),
    path("courses/enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path("my-courses/", views.my_courses, name="my_courses"),
    path("courses/<int:course_id>/lessons/", views.lesson_list, name="lesson_list"),
    path("lessons/<int:lesson_id>/complete/", views.complete_lesson, name="complete_lesson"),
]
