from django.contrib import admin
from .models import Lesson, LessonContent

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'published', 'created_at')
    list_filter = ('course', 'published')
    search_fields = ('title',)

@admin.register(LessonContent)
class LessonContentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'video_url', 'document')
    search_fields = ('lesson__title',)
