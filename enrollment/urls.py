# enrollments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.browse_courses, name='browse_courses'),
    path('courses/my/', views.my_courses, name='my_courses'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('lessons/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path("manage/", views.manage_enrollments, name="manage_enrollments"),
    path("remove/<int:enrollment_id>/", views.remove_enrollment, name="remove_enrollment"),
    path("course/<int:course_id>/", views.course_enrollments, name="course_enrollments"),
    
]
