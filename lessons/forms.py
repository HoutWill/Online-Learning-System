from django import forms
from .models import Lesson, LessonContent
import re
from .models import Assignment , Submission
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'order']

class LessonContentForm(forms.ModelForm):
    class Meta:
        model = LessonContent
        fields = ['description', 'video_url', 'document']

    def clean_video_url(self):
        url = self.cleaned_data.get("video_url")

        if url:
            # Allow YouTube normal URL or embed URL
            if not re.match(r'https?://(www\.)?(youtube\.com|youtu\.be)/', url):
                raise forms.ValidationError("Please enter a valid YouTube URL.")
        return url
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["file"]