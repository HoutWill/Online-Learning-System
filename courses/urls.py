from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.course_add_edit, name="course_add"),
    path("edit/<int:pk>/", views.course_add_edit, name="course_edit"),
    path("delete/<int:pk>/", views.course_delete, name="course_delete"),
    path('category/add',views.category_add,name="category_add"),
    path('course/<int:course_id>/reviews/', views.course_review, name='course_review'),
    path('category/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:category_id>/delete/', views.category_delete, name='category_delete'),
]
