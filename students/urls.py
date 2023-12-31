from django.urls import path
from . import views

app_name = "students"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:student_id>/", views.view_student, name="view_student"),
    path("add/", views.add, name="add"),
    path("edit/<int:student_id>/", views.edit, name="edit"),
    path("delete/<int:student_id>/", views.delete, name="delete"),
]
