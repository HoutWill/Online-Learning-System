from django.urls import path
from . import views

urlpatterns = [
    # Lessons
    path('course/<int:course_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('course/<int:course_id>/lesson/add/', views.lesson_add_edit, name='lesson_add'),
    path('lesson/<int:lesson_id>/edit/', views.lesson_add_edit, name='lesson_edit'),
    path('lesson/<int:lesson_id>/content/', views.lesson_content_edit, name='lesson_content_edit'),
    path('lesson/<int:pk>/detail/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),

    # Assignments
    path('course/<int:course_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('course/<int:course_id>/assignment/add/', views.assignment_add_edit, name='assignment_add_edit'),
    path('assignment/<int:assignment_id>/edit/', views.assignment_add_edit, name='assignment_edit'),
    path('assignment/<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete'),
    path('assignment/<int:assignment_id>/submit/', views.submission_add, name='submission_add'),
    path('assignments/<int:assignment_id>/submissions/', views.submission_list, name='submission_list'),
    path('course/<int:course_id>/my-submissions/', views.my_submissions, name='my_submissions'),

]
