from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='profile'),

    # Employee management
    path('employee/users/', views.user_list, name='user_list'),
    path('employee/users/add/', views.user_add, name='user_add'),
    path('employee/users/delete/<int:pk>/', views.user_delete, name='user_delete'),

    path('employee/courses/', views.course_list_employee, name='course_list_employee'),
    path('employee/enrollments/', views.enrollment_list, name='enrollment_list'),
    
    path("profile/", views.profile_view, name="profile_view"),
    
]
