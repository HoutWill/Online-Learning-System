from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Instructor, Employee

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin class for the User model to include the 'role' field.
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    list_display = BaseUserAdmin.list_display + ('role',)
    list_filter = BaseUserAdmin.list_filter + ('role',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin class for the Student model.
    """
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """
    Admin class for the Instructor model.
    """
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Admin class for the Employee model.
    """
    list_display = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
