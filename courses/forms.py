from django import forms
from .models import Course 
from .models import CourseReview
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'description', 'price', 'image', 'published_status']


class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }